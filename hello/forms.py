# myapp/forms.py

from django import forms
from .models import Item
from .models import Inventory

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name','gtin','image','imageurl']

class AddToInventory(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['gtin', 'location', 'buy_date', 'expiry_date']