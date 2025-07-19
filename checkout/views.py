from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.conf import settings
from .forms import OrderForm
from user_profile.forms import AddressForm
from .models import Order, OrderLineItem
from supplies.models import Supply
from bag.contexts import bag_contents
import stripe


def checkout(request):
    """view to display the checkout page if the bag i not empty"""

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        order_form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
        }
        address_form_data = {
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(order_form_data)
        address_form = AddressForm(address_form_data)
        if order_form.is_valid() and address_form.is_valid():
            with transaction.atomic():
                # First, save the address form
                address = address_form.save()

                # Then, save the order form with the address associated
                order = order_form.save(commit=False)
                order.address = address
                order.save()
                for item_id, item_data in bag.items():
                    try:
                        supply = Supply.objects.get(id=item_id)
                        for renting_date, date_item in item_data:
                            for renting_days, days_item in date_item:
                                order_line_item = OrderLineItem(
                                    order=order,
                                    supply=supply,
                                    price_per_day=supply.price_per_day,
                                    quantity=days_item['quantity'],
                                    renting_days=renting_days,
                                    start_renting_date=renting_date,
                                )
                                order_line_item.save()
                    except Supply.DoesNotExist:
                        messages.error(request, (
                            "One of the Supplies in your bag wasn't found in our database. "
                            "Please call us for assistance!")
                        )
                        order.delete()
                        return redirect(reverse('view_bag'))

                request.session['save_info'] = 'save-info' in request.POST
                return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    else:

        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('supplies'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)

        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()
        address_form = AddressForm()
        template = 'checkout/checkout.html'

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set it in your environment?')

        context = {
            'order_form': order_form,
            'address_form': address_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }
    return render(request, template, context)
