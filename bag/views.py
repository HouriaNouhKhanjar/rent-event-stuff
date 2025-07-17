from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from supplies.models import Supply


# Create your views here.
BAG_KEY = "bag"
ID_KEY = "id"
QTY_KEY = "quantity"
DATE_KEY = "start_renting_date"
DAYS_KEY = "renting_days"


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def check_item_in_bag(item, bag):
    """Check if item already exist in the shoping bag"""

    updated = False

    supply_id = item[ID_KEY]
    del item[ID_KEY]
    renting_date = item[DATE_KEY]
    days = item[DAYS_KEY]
    message = ""

    if supply_id in list(bag.keys()):
        bag_item = bag[supply_id]
        if renting_date in list(bag_item.keys()):
            if days in list(bag_item[renting_date].keys()):
                bag[supply_id][renting_date][days][QTY_KEY] += item[QTY_KEY]
                message = f'Updated quantity to {bag[supply_id][renting_date][days][QTY_KEY]}, '
                updated = True
        else:
            bag[supply_id].update({renting_date: {}})

        if not updated:
            bag[supply_id][renting_date].update({days: {}})
            bag[supply_id][renting_date][days].update({QTY_KEY: item[QTY_KEY]})
            message = f'Added new quantity: {bag[supply_id][renting_date][days][QTY_KEY]}, '

    else:
        bag.update({supply_id: {}})
        bag[supply_id].update({renting_date: {}})
        bag[supply_id][renting_date].update({days: {}})
        bag[supply_id][renting_date][days].update({QTY_KEY: item[QTY_KEY]})
        message = f'Added new quantity: {bag[supply_id][renting_date][days][QTY_KEY]}, '

    message += f'on date: {item[DATE_KEY]}, for {item[DAYS_KEY]} days, '

    return message


def add_to_bag(request, item_id):
    """ Add a quantity of the specified supply,
    the startand end renting date to the
    shopping bag """

    supply = get_object_or_404(Supply, pk=item_id)
    supply_name = (supply.name[:75] + '..') if len(supply.name) > 75 else supply.name

    item = {}
    item[ID_KEY] = item_id
    item[QTY_KEY] = int(request.POST.get(QTY_KEY))
    item[DAYS_KEY] = request.POST.get(DAYS_KEY)
    item[DATE_KEY] = request.POST.get(DATE_KEY)
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get(BAG_KEY, {})
    message = check_item_in_bag(item, bag)

    request.session[BAG_KEY] = bag
    messages.success(request, f'{message} for supply item: {supply_name}')
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified supply
    to the specified renting date and days"""

    supply = get_object_or_404(Supply, pk=item_id)
    supply_name = (supply.name[:75] + '..') if len(supply.name) > 75 else supply.name

    item = {}
    item[QTY_KEY] = int(request.POST.get(QTY_KEY))
    item[DAYS_KEY] = request.POST.get(DAYS_KEY)
    item[DATE_KEY] = request.POST.get(DATE_KEY)
    bag = request.session.get('bag', {})
    message = ''

    if item[QTY_KEY] > 0:
        bag[item_id][item[DATE_KEY]][item[DAYS_KEY]][QTY_KEY] = item[QTY_KEY]
        message = f'Updated quantity to {bag[item_id][item[DATE_KEY]][item[DAYS_KEY]][QTY_KEY]}, '
        message += f'on date: {item[DATE_KEY]}, for supply item: {supply_name}'

    else:
        del bag[item_id][item[DATE_KEY]][item[DAYS_KEY]]
        message = f'Delete quantity for {item[DAYS_KEY]} days, '
        if not bag[item_id][item[DATE_KEY]]:
            del bag[item_id][item[DATE_KEY]]
            message = f'Delete renting date: {item[DATE_KEY]}, '
        else:
            message += f'on date: {item[DATE_KEY]}, '

        if not bag[item_id]:
            bag.pop(item_id)
            message = f'Delete item: {supply_name} from bag'

        else:
            message += f'for supply item: {supply_name}'

    messages.success(request, f'{message}')
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""
    try:
        supply = get_object_or_404(Supply, pk=item_id)
        supply_name = (supply.name[:75] + '..') if len(supply.name) > 75 else supply.name

        item = {}
        item[DAYS_KEY] = request.POST.get(DAYS_KEY)
        item[DATE_KEY] = request.POST.get(DATE_KEY)
        bag = request.session.get('bag', {})
        message = ''

        del bag[item_id][item[DATE_KEY]][item[DAYS_KEY]]
        message = f'Delete quantity for renting days {item[DAYS_KEY]}, '
        if not bag[item_id][item[DATE_KEY]]:
            del bag[item_id][item[DATE_KEY]]
            message = f'Delete quantity for renting on date: {item[DATE_KEY]}, '
        else:
            message += f'on {item[DATE_KEY]}, '
        if not bag[item_id]:
            bag.pop(item_id)
            message = f'Delete renting on date: {item[DATE_KEY]} for {item[DAYS_KEY]} days, for supply item {supply_name}'
        else:
            message += f'for supply item {supply_name}'

        messages.success(request, f'{message}')
        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)
