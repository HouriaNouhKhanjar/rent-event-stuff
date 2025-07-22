from django import forms
from .models import Address, UserProfile
import random
import string


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county', )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)

        placeholders = {
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County | State or Locality',
        }
        
        excluded_fields = ['country', 'user', 'is_default', 'type']

        # Generate a random prefix
        random_prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        for field in self.fields:
            field_item = self.fields[field]
            if field not in excluded_fields:
                if field_item.required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
            # Check if the field already has an id and modify it
            if 'id' in field_item.widget.attrs:
                field_item.widget.attrs['id'] = f'{random_prefix}_{field_item.widget.attrs["id"]}'
            else:
                # If no id is set, set a new id with the random prefix
                field_item.widget.attrs['id'] = f'{random_prefix}_{field}'

            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False


class UserAddressForm(AddressForm):
    class Meta(AddressForm.Meta):
        fields = AddressForm.Meta.fields + ('user', 'type', 'is_default', )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'phone_number': 'Phone Number',
        }

        self.fields['phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'profile-form-input'
            self.fields[field].label = False
