from django.shortcuts import render, get_object_or_404
from .models import Supply


def all_supplies(request):
    """ A view to return the supplies page """
    supplies = Supply.objects.all()

    context = {
        'supplies': supplies
    }

    return render(request, 'supplies/supplies.html', context)


def supply_detail(request, supply_id):
    """ A view to return supply detail page """
    supply = get_object_or_404(Supply, pk=supply_id)

    context = {
        'supply': supply
    }

    return render(request, 'supplies/supply-detail.html', context)
