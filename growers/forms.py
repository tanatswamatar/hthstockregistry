from django import forms
from .models import Grower

class AllocationForm(forms.Form):
    grower_no = forms.CharField(
        label="Grower Number",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Grower Number'})
    )
    delivery_note = forms.CharField(
        label="Delivery Note #",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional DN Number'})
    )
