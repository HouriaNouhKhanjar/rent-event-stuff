from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, Address, SavedSupply
from .forms import UserProfileForm, UserAddressForm
from supplies.models import Supply
from checkout.models import Order


def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    billing_address_form = UserAddressForm()
    delivery_address_form = UserAddressForm()

    billing_address = None
    delivery_address = None
    billing_address = Address.objects.filter(type=0, user=request.user,
                                             is_default=True).first()
    if billing_address:
        billing_address_form = UserAddressForm(instance=billing_address)
    delivery_address = Address.objects.filter(type=1, user=request.user,
                                              is_default=True).first()
    if delivery_address:
        delivery_address_form = UserAddressForm(instance=delivery_address)

    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'user_profile_form': form,
        'billing_address_form': billing_address_form,
        'delivery_address_form': delivery_address_form,
        'billing_address': billing_address,
        'delivery_address': delivery_address,
        'show_only_message': True,
        'orders': orders
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


def update_address(request):
    """Update users billing or delivery address"""

    if request.method == 'POST':

        address_form_data = {
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
            'type': int(request.POST['type']),
            'is_default': True,
            'user': request.user
        }
        form = UserAddressForm(address_form_data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the address is valid.')

    return redirect(reverse('profile'))


@login_required
def toggle_save_supply(request, supply_id):
    supply = get_object_or_404(Supply, id=supply_id)

    # Check if supply is already saved
    saved_item = SavedSupply.objects.filter(user=request.user,
                                            supply=supply).first()

    if saved_item:
        # If it's saved, delete it (remove from saved items)
        saved_item.delete()
        messages.info(request, 'Supply removed from your saved list.')
    else:
        # If it's not saved, create it
        SavedSupply.objects.create(user=request.user, supply=supply)
        messages.info(request, 'Supply added to your saved list.')

    return redirect('supply_detail', supply_id=supply.id)
