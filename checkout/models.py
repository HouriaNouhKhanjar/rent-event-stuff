import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from supplies.models import Supply
from user_profile.models import Address


ORDER_STATUS = ((0, "Pending"), (1, "Approved"), (2, "Cancelled"),
                (3, "Succeed"), (4, "Failed"), )


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    billing_address = models.ForeignKey(Address,
                                        on_delete=models.SET_NULL,
                                        related_name='billing_orders',
                                        null=True,
                                        blank=True)
    delivery_address = models.ForeignKey(Address,
                                         on_delete=models.SET_NULL,
                                         related_name='delivery_orders',
                                         null=True,
                                         blank=True)
    status = models.IntegerField(choices=ORDER_STATUS, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum']
        if self.order_total:
            if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
                self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
            else:
                self.delivery_cost = 0
            self.grand_total = self.order_total + self.delivery_cost
            self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    supply = models.ForeignKey(Supply, null=False,
                               blank=False, on_delete=models.CASCADE)
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         null=False, blank=False,
                                         editable=False)
    renting_days = models.IntegerField(null=False, blank=False, default=0)
    start_renting_date = models.DateField(null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.price_per_day = self.supply.price_per_day
        self.lineitem_total = self.supply.price_per_day * self.quantity * self.renting_days
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.supply.sku} on order {self.order.order_number}'
