from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Supply, Category


def all_supplies(request):
    """ A view to return the supplies page """
    supplies = Supply.objects.all()
    query = ''
    categories = None

    if 'category' in request.GET:
        category = get_object_or_404(Category, slug=request.GET['category'])
        if category.is_main:
            # Get all subcategories and the main category itself
            subcategories = category.subcategories.all()
            supplies = Supply.objects.filter(category__in=[category] + list(subcategories))
            categories = [category, list(subcategories)]
         
        else:
            # Subcategory: just filter supplies by this category
            supplies = Supply.objects.filter(category=category)
            categories = category

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
        'current_categories': categories,
    }

    return render(request, 'supplies/supplies.html', context)


def supply_detail(request, supply_id):
    """ A view to return supply detail page """
    supply = get_object_or_404(Supply, pk=supply_id)

    context = {
        'supply': supply
    }

    return render(request, 'supplies/supply-detail.html', context)
