from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from supplies.models import Supply


def bag_contents(request):

    bag_items = []
    total = 0
    supply_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_obj in bag.items():
        supply = get_object_or_404(Supply, pk=item_id)
        total += item_obj['quantity'] * supply.price_per_day
        supply_count += item_obj['quantity']
        bag_items.append({
            'item_id': item_id,
            'quantity': item_obj['quantity'],
            'supply': supply,
        })

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
