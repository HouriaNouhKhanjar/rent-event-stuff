from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from .models import UserProfile, Address
from .forms import UserProfileForm, UserAddressForm
from checkout.models import Order


def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    user_profile_form = UserProfileForm(instance=profile)
    billing_address_form = UserAddressForm()
    delivery_address_form = UserAddressForm()

    billing_address = None
    delivery_address = None
    billing_address = Address.objects.filter(type=0, user=request.user).first()
    if billing_address:
        billing_address_form = UserAddressForm(instance=billing_address)
    delivery_address = Address.objects.filter(type=1, user=request.user).first()
    if delivery_address:
        delivery_address_form = UserAddressForm(instance=delivery_address)

    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'user_profile_form': user_profile_form,
        'billing_address_form': billing_address_form,
        'delivery_address_form': delivery_address_form,
        'billing_address': billing_address,
        'delivery_address': delivery_address,
        'on_profile_page': True,
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
        id = request.POST['address_id']
        address = None
        if id:
            address = get_object_or_404(Address, pk=id)

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
        form = UserAddressForm(address_form_data, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    return redirect(reverse('profile'))
