from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'full_name', 'phone', 'address_line_1',
            'city', 'state', 'country', 'pincode', 'address_type', 'is_default'
        ]
