from django.contrib import admin
from .models import Address, UserProfile


class AddressAdmin(admin.ModelAdmin):
    readonly_fields = ('created_on', )

    list_display = ('title', 'postcode', 'town_or_city',
                    'type', 'created_on')

    ordering = ('-created_on', )

    search_fields = ['postcode', 'town_or_city', 'country']
    list_editable = ('type',)
    list_filter = ('created_on', 'type', )
    list_per_page = 15


class UserProfileAdmin(admin.ModelAdmin):

    list_display = ('user', 'phone_number',)

    search_fields = ['user__username', 'phone_number']
    list_per_page = 15


admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
