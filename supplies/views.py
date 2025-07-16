from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Supply, Category


def all_supplies(request):
    """ A view to return the supplies including sorting and search queries """

    supplies = Supply.objects.all()
    query = ''
    category = None
    category_slug = ''
    current_categories = []
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                supplies = supplies.annotate(lower_name=Lower('name'))

            if sortkey == 'category':
                sortkey = 'category__slug'

            if sortkey == 'price':
                sortkey = 'price_per_day'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            supplies = supplies.order_by(sortkey)

        if 'category' in request.GET:
            category = get_object_or_404(Category, slug=request.GET['category'])
            category_slug = category.get_slug()
            if category.is_main:
                # Get all subcategories and the main category itself
                subcategories = category.subcategories.all()
                current_categories = [category] + list(subcategories)
                supplies = supplies.filter(category__in=current_categories)

            else:
                # Subcategory: just filter supplies by this category
                current_categories = [category]
                supplies = supplies.filter(category=category)

        if 'categories' in request.GET:
            categories = request.GET['categories'].split(',')
            category_slug = ''
            supplies = supplies.filter(category__slug__in=categories)
            current_categories = Category.objects.filter(slug__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               "You didn't enter any search criteria!")
                return redirect(reverse('supplies'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            supplies = supplies.filter(queries)

    current_sorting = f'{sort}_{direction}'

    paginator = Paginator(supplies, 24)

    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'supplies_count': len(supplies),
        'supplies': page_obj.object_list,
        'search_term': query,
        'category_slug': category_slug,
        'current_categories': current_categories,
        'current_sorting': current_sorting,
        'page_obj': page_obj
    }

    return render(request, 'supplies/supplies.html', context)


def supply_detail(request, supply_id):
    """ A view to return supply detail page """
    supply = get_object_or_404(Supply, pk=supply_id)

    context = {
        'supply': supply
    }

    return render(request, 'supplies/supply-detail.html', context)
