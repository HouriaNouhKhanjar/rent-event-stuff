from django.contrib import admin
from .models import Address


class AddressAdmin(admin.ModelAdmin):
    readonly_fields = ('created_on', )

    list_display = ('title', 'postcode', 'town_or_city', 'street_address1',
                    'type', )

    ordering = ('-created_on', )

    search_fields = ['postcode', 'town_or_city', 'country']
    list_editable = ('type',)
    list_filter = ('created_on', 'type', )
    list_per_page = 15


admin.site.register(Address, AddressAdmin)
