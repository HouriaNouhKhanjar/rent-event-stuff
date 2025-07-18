from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem

    readonly_fields = ('lineitem_total', 'price_per_day')

    fields = ('supply',
              ('start_renting_date', 'renting_days'),
              'quantity', 'price_per_day', 'lineitem_total', )


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'created_on',
                       'delivery_cost', 'order_total',
                       'grand_total',)

    fields = ('order_number', 'full_name',
              'email', 'phone_number', 'billing_address',
              'delivery_address', 'delivery_cost', 'status',
              'order_total', 'grand_total',)

    list_display = ('order_number', 'created_on', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total', 'status', )

    ordering = ('-created_on',)

    list_editable = ('status',)
    search_fields = ['order_number', 'full_name', 'phone_number', 'email']
    list_filter = ('created_on', 'status', )
    list_per_page = 15


admin.site.register(Order, OrderAdmin)
