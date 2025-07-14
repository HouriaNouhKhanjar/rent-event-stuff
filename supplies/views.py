from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Supply


def all_supplies(request):
    """ A view to return the supplies page """
    supplies = Supply.objects.all()
    query = ''

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               "You didn't enter any search criteria!")
                return redirect(reverse('supplies'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            supplies = supplies.filter(queries)

    context = {
        'supplies': supplies,
        'search_term': query,
    }

    return render(request, 'supplies/supplies.html', context)


def supply_detail(request, supply_id):
    """ A view to return supply detail page """
    supply = get_object_or_404(Supply, pk=supply_id)

    context = {
        'supply': supply
    }

    return render(request, 'supplies/supply-detail.html', context)
