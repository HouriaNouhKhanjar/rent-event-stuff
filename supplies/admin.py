from django.contrib import admin
from .models import Supply, Category

# Register your models here.


class SupplyAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price_per_day',
        'quantity_available'
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )


admin.site.register(Supply, SupplyAdmin)
admin.site.register(Category, CategoryAdmin)
