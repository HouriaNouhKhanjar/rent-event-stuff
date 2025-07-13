from django.shortcuts import render
from .models import Supply


def all_supplies(request):
    """ A view to return the supplies page """
    supplies = Supply.objects.all()

    context = {
        'supplies': supplies
    }

    return render(request, 'supplies/supplies.html', context)
