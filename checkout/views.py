from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
from user_profile.forms import AddressForm
from bag.contexts import bag_contents

import stripe


def checkout(request):
    """view to display the checkout page if the bag i not empty"""
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('supplies'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)

    order_form = OrderForm()
    address_form = AddressForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'address_form': address_form,
        'stripe_public_key': 'pk_test_51RmKsi097A1V6ZA75q4vDrhCiYIIU6igAJHdaEkfjYOjzWiJ3vAY9JHvJHV4yV4wx8UQrXIALujOgF1mEDHKWPSJ00OngrIQ3w',
        'client_secret': 'this is my secrete key',
    }

    return render(request, template, context)
