from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from supplies.models import Supply


BAG_KEY = "bag"
ID_KEY = "id"
QTY_KEY = "quantity"
DATE_KEY = "start_renting_date"
DAYS_KEY = "renting_days"


def get_bag_items(bag):

    bag_items = []
    total = 0
    supply_count = 0

    for item_id, item_obj in bag.items():
        id = int(item_id)
        supply = get_object_or_404(Supply, pk=id)
        for date, days_obj in item_obj.items():
            for days, quantity_data in days_obj.items():
                sub_total = int(days) * quantity_data[QTY_KEY] * supply.price_per_day
                total += sub_total
                supply_count += quantity_data[QTY_KEY]
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity_data[QTY_KEY],
                    'renting_days': days,
                    'start_renting_date': date,
                    'sub_total': sub_total,
                    'supply': supply,
                })

    return bag_items, total, supply_count


def bag_contents(request):

    bag = request.session.get(BAG_KEY, {})

    bag_items, total, supply_count = get_bag_items(bag)

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'supply_count': supply_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
