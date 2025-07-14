from .models import Category
from django.db.models import Count, Q, Prefetch


def navbar_categories(request):
    """ Get the categories orderd by supplies count """

    # Get only the categories which has supplies
    sub_qs = Category.objects.annotate(
        supply_count=Count('supply')
        ).filter(supply_count__gt=0)

    # Get only main categories and sort them by whichever has the most supplies
    main_categories = Category.objects.filter(parent__isnull=True).annotate(
        direct_count=Count('supply'),
        sub_count=Count('subcategories__supply')
    ).filter(
        Q(direct_count__gt=0) | Q(sub_count__gt=0)
    ).prefetch_related(
        Prefetch('subcategories', queryset=sub_qs)
    ).order_by('-direct_count', '-sub_count')

    # get the first two categories
    top_categories = main_categories[:2]

    # get other categories
    other_categories = main_categories[2:]

    return {
        'top_categories': top_categories,
        'other_categories': other_categories,
    }
