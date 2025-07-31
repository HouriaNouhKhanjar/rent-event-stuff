from django.contrib import admin
from .models import Supply, Category, SupplyImage, Review
from .forms import SupplyImageInlineForm

# Register your models here.


class SupplyImageInline(admin.StackedInline):
    """
    Displays the supply image form in supply edit page as inline form.
    """
    model = SupplyImage
    form = SupplyImageInlineForm
    readonly_fields = ('image_url', 'created_on', )
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
    readonly_fields = ('created_on', )
    search_fields = ['name', 'description', 'category']
    list_filter = ('created_on', 'category',)
    list_per_page = 15


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    readonly_fields = ('slug', 'created_on', )
    search_fields = ['name']
    list_per_page = 10


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'supply',
        'rating',
        'created_at'
    )
    readonly_fields = ('created_at', )
    list_per_page = 10


admin.site.register(Supply, SupplyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
