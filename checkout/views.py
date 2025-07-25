from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction
from django.conf import settings
from .forms import OrderForm
from user_profile.forms import AddressForm, UserProfileForm, UserAddressForm
from user_profile.models import UserProfile, Address
from .models import Order, OrderLineItem
from supplies.models import Supply
from bag.contexts import bag_contents
import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """view to display the checkout page if the bag is not empty"""

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        order_form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
        }
        save_info = request.POST.get('save-info')
        is_default = save_info.lower() in ['true', '1', 'on'] if save_info else False
        address_form_data = {
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
            'user': request.user,
            'is_defalut': is_default,
            'type': 0
        }
        order_form = OrderForm(order_form_data)
        billing_address_form = UserAddressForm(address_form_data)
        address_form_data['type'] = 1
        delivery_address_form = UserAddressForm(address_form_data)
        if order_form.is_valid() and billing_address_form.is_valid():
            with transaction.atomic():
                billing_address = billing_address_form.save()

                delivery_address = delivery_address_form.save()

                order = order_form.save(commit=False)
                order.billing_address = billing_address
                order.delivery_address = delivery_address
                pid = request.POST.get('client_secret').split('_secret')[0]
                order.stripe_pid = pid
                order.original_bag = json.dumps(bag)
                order.save()
                for item_id, item_data in bag.items():
                    try:
                        supply = Supply.objects.get(id=item_id)
                        for renting_date, date_item in item_data.items():
                            for renting_days, days_item in date_item.items():
                                order_line_item = OrderLineItem(
                                    order=order,
                                    supply=supply,
                                    price_per_day=supply.price_per_day,
                                    quantity=int(days_item['quantity']),
                                    renting_days=int(renting_days),
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

                request.session['save_info'] = request.POST.get('save-info', None)
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

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.phone_number,
                })
                delivery_address = None
                delivery_address = Address.objects.filter(type=1,
                                                          user=request.user,
                                                          is_default=True).first()
                if delivery_address:
                    address_form = AddressForm(initial={
                        'country': delivery_address.country,
                        'postcode':delivery_address.postcode,
                        'town_or_city': delivery_address.town_or_city,
                        'street_address1': delivery_address.street_address1,
                        'street_address2': delivery_address.street_address2,
                        'county': delivery_address.county,
                    })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set it in your environment?')

        context = {
            'order_form': order_form,
            'address_form': address_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        template = 'checkout/checkout.html'
        return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        is_default_address = save_info.lower() in ['true', '1', 'on'] if save_info else False
        if is_default_address:
            profile_data = {
                'phone_number': order.phone_number,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

            order.delivery_address.is_default = True
            order.delivery_address.user = order.user_profile.user
            order.billing_address.is_default = True
            order.billing_address.user = order.user_profile.user

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
