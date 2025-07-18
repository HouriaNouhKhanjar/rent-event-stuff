from django.db import models
from django.contrib.auth.models import User

ADDRESS_TYPE = ((0, "Billing"), (1, "Delivery"))


class Address(models.Model):

    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True,
                             related_name="user_addresses",
                             on_delete=models.CASCADE)
    type = models.IntegerField(choices=ADDRESS_TYPE, default=0)
    is_default = models.BooleanField(default=False)
