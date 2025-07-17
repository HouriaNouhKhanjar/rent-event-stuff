from django.shortcuts import render, redirect, reverse, HttpResponse

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

    if supply_id in list(bag.keys()):
        bag_item = bag[supply_id]
        if renting_date in list(bag_item.keys()):
            if days in list(bag_item[renting_date].keys()):
                bag[supply_id][renting_date][days][QTY_KEY] += item[QTY_KEY]
                updated = True
        else:
            bag[supply_id].update({renting_date: {}})

        if not updated:
            bag[supply_id][renting_date].update({days: {}})
            bag[supply_id][renting_date][days].update({QTY_KEY: item[QTY_KEY]})
    else:
        bag.update({supply_id: {}})
        bag[supply_id].update({renting_date: {}})
        bag[supply_id][renting_date].update({days: {}})
        bag[supply_id][renting_date][days].update({QTY_KEY: item[QTY_KEY]})


def add_to_bag(request, item_id):
    """ Add a quantity of the specified supply,
    the startand end renting date to the
    shopping bag """

    item = {}
    item[ID_KEY] = item_id
    item[QTY_KEY] = int(request.POST.get(QTY_KEY))
    item[DAYS_KEY] = request.POST.get(DAYS_KEY)
    item[DATE_KEY] = request.POST.get(DATE_KEY)
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get(BAG_KEY, {})
    check_item_in_bag(item, bag)

    request.session[BAG_KEY] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified supply
    to the specified renting date and days"""

    item = {}
    item[QTY_KEY] = int(request.POST.get(QTY_KEY))
    item[DAYS_KEY] = request.POST.get(DAYS_KEY)
    item[DATE_KEY] = request.POST.get(DATE_KEY)
    bag = request.session.get('bag', {})

    if item[QTY_KEY] > 0:
        bag[item_id][item[DATE_KEY]][item[DAYS_KEY]][QTY_KEY] = item[QTY_KEY]
    else:
        del bag[item_id][item[DATE_KEY]][item[DAYS_KEY]]
        if not bag[item_id][item[DATE_KEY]]:
            del bag[item_id][item[DATE_KEY]]
        if not bag[item_id]:
            bag.pop(item_id)
    print(bag)
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""
    try:
        item = {}
        item[DAYS_KEY] = request.POST.get(DAYS_KEY)
        item[DATE_KEY] = request.POST.get(DATE_KEY)
        bag = request.session.get('bag', {})
    
        print(item)
        del bag[item_id][item[DATE_KEY]][item[DAYS_KEY]]
        if not bag[item_id][item[DATE_KEY]]:
            del bag[item_id][item[DATE_KEY]]
        if not bag[item_id]:
            bag.pop(item_id)

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)
