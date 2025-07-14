from django import forms
from .models import SupplyImage


class SupplyImageInlineForm(forms.ModelForm):
    """
    Customize image upload form using
    custom :widdget:`widgets.DragAndDropWidget`.
    """
    class Meta:
        model = SupplyImage
        fields = '__all__'
