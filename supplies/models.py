from django.core.files.storage import default_storage
from functools import cached_property
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.db import models


class Category(models.Model):
    """
    Stores a single category entry.
    """
    name = models.CharField(max_length=254, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    parent = models.ForeignKey('self',
                               related_name='subcategories',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def is_main(self):
        return self.parent is None

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
    sku = models.CharField(max_length=254, null=False, blank=False)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2)

    quantity_available = models.IntegerField(default=1,
                                             validators=[MinValueValidator(1)],
                                             null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name[0:50]}...' if len(self.name) > 50 else self.name

    @cached_property
    def image_url(self):
        """ Returns the first image URL if available """
        first_image = self.images.first()
        if first_image:
            return first_image.image.url
        return '/media/placeholder.jpg'

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

    def save(self, *args, **kwargs):
        # If the image field is not empty, set the image_url field
        if self.image and not self.image_url:
            self.image_url = default_storage.url(self.image.name)

        super(SupplyImage, self).save(*args, **kwargs)
