from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Supply, Category, SupplyImage, Review
from user_profile.models import SavedSupply
from checkout.models import Order
from .forms import SupplyForm, ReviewForm


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

    saved_item = None
    can_make_review = None
    review_form = None
    if request.user.is_authenticated:
        saved_item = SavedSupply.objects.filter(user=request.user,
                                                supply=supply).first()
        can_make_review = Order.objects.filter(user_profile__user=request.user,
                                               lineitems__supply=supply).exists()
        review_form = ReviewForm()

    context = {
        'supply': supply,
        'saved_item': saved_item,
        'can_make_review': can_make_review,
        'review_form': review_form
    }

    return render(request, 'supplies/supply-detail.html', context)


def add_supply(request):
    """ manage add a supply to the store """
    supply = None
    edit_mode = False
    form = SupplyForm()

    if request.method == 'POST':
        form = SupplyForm(request.POST, request.FILES)
        if form.is_valid():
            supply = form.save()
            images = request.FILES.getlist('images')
            for img in images:
                SupplyImage.objects.create(supply=supply, image=img)
            messages.success(request, 'Successfully added supply!')
            return redirect('edit_supply', supply.id)
        else:
            messages.error(request, 'Failed to add supply. Please ensure the form is valid.')

    template = 'supplies/supply-form.html'
    context = {
        'form': form,
        'supply': supply,
        'show_only_message': True,
        'edit_mode': edit_mode,
    }

    return render(request, template, context)


def edit_supply(request, supply_id):
    """ manage add or edit a supply to the store """
    supply = None
    edit_mode = False
    form = SupplyForm()

    if request.method == 'POST':
        edit_mode = True
        supply = get_object_or_404(Supply, pk=supply_id)

        form = SupplyForm(request.POST, request.FILES, instance=supply)
        if form.is_valid():
            supply = form.save()
            images = request.FILES.getlist('images')
            for img in images:
                SupplyImage.objects.create(supply=supply, image=img)
            messages.success(request, 'Successfully updated supply!')
            return redirect('edit_supply', supply.id)
        else:
            messages.error(request, 'Failed to update supply. Please ensure the form is valid.')

    else:
        edit_mode = True
        supply = get_object_or_404(Supply, pk=supply_id)
        form = SupplyForm(instance=supply)

    template = 'supplies/supply-form.html'
    context = {
        'form': form,
        'supply': supply,
        'show_only_message': True,
        'edit_mode': edit_mode,
    }

    return render(request, template, context)


def delete_supply_image(request, pk):
    """
    Delete an individual image.

    **args**

    ``pk``
        The instance id of :model:`supplies.SupplyImage` to delete.
    """
    if request.method not in ["POST", "DELETE"]:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    image = get_object_or_404(SupplyImage, pk=pk)

    # Check if the logged-in user is admin
    if not (request.user and request.user.is_superuser):
        return JsonResponse({'error': 'Forbidden'}, status=403)

    try:
        image.delete()
        messages.success(request,
                         "Image deleted successfully.")
        return JsonResponse({'success': True})
    except Exception as e:
        messages.error(request, f"image deletion failed: {e}")
        return JsonResponse({'error': f'deletion failed: {e}'},
                            status=500)


def delete_supply(request, pk):
    """
    Delete an individual supply.

    **args**

    ``pk``
        The instance id of :model:`supplies.Supply` to delete.
    """
    if request.method not in ["POST", "DELETE"]:
        messages.info(request, 'Method not allowed')
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    supply = get_object_or_404(Supply, pk=pk)

    # Check if the logged-in user is admin
    if not (request.user and request.user.is_superuser):
        messages.info(request, 'Forbidden')
        return JsonResponse({'error': 'Forbidden'}, status=403)

    try:
        supply.delete()
        messages.info(request, "Supply deleted successfully.")
        return JsonResponse({'message': 'Deleted Successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': f'Supply deletion failed: {e}'},
                            status=500)


@login_required
def review_supply(request, supply_id):
    if request.method == 'POST':
        supply = get_object_or_404(Supply, id=supply_id)

        rented = Order.objects.filter(user_profile__user=request.user,
                                      lineitems__supply=supply).exists()

        if rented:
            review = Review.objects.filter(user=request.user, supply=supply).first()

            form = None
            if review:
                form = ReviewForm(request.POST, instance=review)
            else:
                form = ReviewForm(request.POST)

            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.supply = supply
                review.save()

                messages.info(request, 'Your review has been submitted.')
                return redirect('supply_detail', supply_id=supply.id)
            else:
                messages.error(request, "Can not submit your Review.")
                return redirect('supply_detail', supply_id=supply.id)

        else:
            messages.error(request, "Sorry, You dont have the permission to review this item.")
            return redirect('supply_detail', supply_id=supply.id)

    messages.error(request, "Method Not Allowed.")
    return redirect('supply_detail', supply_id=supply.id)
