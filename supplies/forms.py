from django import forms
from .models import SupplyImage, Supply


class SupplyImageInlineForm(forms.ModelForm):
    """
    Customize image upload form using
    custom :widdget:`widgets.DragAndDropWidget`.
    """
    class Meta:
        model = SupplyImage
        fields = '__all__'


class SupplyForm(forms.ModelForm):

    images = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'allow_multiple_selected': True}), required=False)

    class Meta:
        model = Supply
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'category': 'Category',
            'sku': 'SKU',
            'name': 'Supply Name',
            'description': 'Supply Description',
            'price_per_day': 'Price Per Day',
            'quantity_available': 'Available Quantity',
            'images': 'Images',
        }

        self.fields['category'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'supply-input'
            self.fields[field].label = False
