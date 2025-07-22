from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver

ADDRESS_TYPE = ((0, "Billing"), (1, "Delivery"))


class Address(models.Model):

    country = CountryField(blank_label='Country *', null=False, blank=False)
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

    @property
    def title(self):
        if self.user:
            return f'Address for {self.user.username}'
        else:
            return f'Address in {self.country}'

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
