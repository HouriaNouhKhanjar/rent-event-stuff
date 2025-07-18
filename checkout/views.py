from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
from user_profile.forms import AddressForm


def checkout(request):
    """view to display the checkout page if the bag i not empty"""
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('supplies'))
    
    order_form = OrderForm()
    address_form = AddressForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'address_form': address_form,
    }

    return render(request, template, context)