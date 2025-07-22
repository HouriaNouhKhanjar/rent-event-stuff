from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm, AddressForm


def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    billing_address_form = AddressForm()
    delivery_address_form = AddressForm()
    user_addresses = profile.user.user_addresses.all()
    if len(user_addresses):
        billing_address = profile.user.user_addresses.filter(type=0)
        if billing_address:
            billing_address_form = AddressForm(isinstance=billing_address)
        delivery_address = profile.user.user_addresses.filter(type=1)
        if delivery_address:
            delivery_address_form = AddressForm(isinstance=delivery_address)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    user_profile_form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'user_profile_form': user_profile_form,
        'billing_address_form': billing_address_form,
        'delivery_address_form': delivery_address_form,
        'on_profile_page': True,
        'orders': orders
    }

    return render(request, template, context)


def update_address(request, address_type):
    """ A view to return supply detail page """
    profile = get_object_or_404(UserProfile, user=request.user)

    context = {
    }

    return render(request, 'profiles/profile.html', context)
