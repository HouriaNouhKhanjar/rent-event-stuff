from django.contrib import admin
from .models import Supply, Category, SupplyImage
from .forms import SupplyImageInlineForm

# Register your models here.


class SupplyImageInline(admin.StackedInline):
    """
    Displays the supply image form in supply edit page as inline form.
    """
    model = SupplyImage
    form = SupplyImageInlineForm
    extra = 1


class SupplyAdmin(admin.ModelAdmin):
    inlines = [SupplyImageInline]
    list_display = (
        'sku',
        'name',
        'category',
        'price_per_day',
        'quantity_available'
    )
    search_fields = ['name', 'description', 'category']
    list_filter = ('created_on', 'category',)
    list_per_page = 15


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ['name']
    list_per_page = 10


admin.site.register(Supply, SupplyAdmin)
admin.site.register(Category, CategoryAdmin)
