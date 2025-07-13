from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Stores a single category entry.
    """
    name = models.CharField(max_length=254, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    parent = models.ForeignKey('Category', null=True, blank=True,
                               on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_slug(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["created_on"]
        verbose_name_plural = "Categories"


class Supply(models.Model):
    """
    Stores a single supply entry related to model:`supply.Category`.
    """
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2)
    quantity_available = models.IntegerField(default=0, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Supplies"


class SupplyImage(models.Model):
    """
    Stores a single supply image entry related to :model:`supply.Supply`.
    """
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE,
                               related_name='images')
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
