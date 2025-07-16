from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """ A view that renders the bag contents page """
    
    return render(request, 'bag/bag.html')


def check_item_in_bag(item, bag):
    """ Check if item already exist in the shoping bag"""

    supply_id = item['id']
    if supply_id in list(bag.keys()):
        bag[supply_id]['quantity'] += item['quantity']
    else:
        bag[supply_id] = item


def add_to_bag(request, item_id):
    """ Add a quantity of the specified supply,
    the startand end renting date to the
    shopping bag """

    item = {}
    item['id'] = item_id
    item['quantity'] = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})
    check_item_in_bag(item, bag)
    print(bag)

    request.session['bag'] = bag
    return redirect(redirect_url)
