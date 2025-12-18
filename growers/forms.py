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


class GrowerForm(forms.ModelForm):
    class Meta:
        model = Grower
        fields = [
            'grower_no', 'surname', 'first_name', 'id_number', 
            'farm', 'area', 'phone', 'hectares', 'field_officer',
            'bank_name', 'branch_name', 'branch_code', 
            'account_number', 'account_holder'
        ]
        # Adding some styling to match Bootstrap
        widgets = {
            field: forms.TextInput(attrs={'class': 'form-control'}) 
            for field in ['bank_name', 'branch_name', 'branch_code', 'account_number', 'account_holder']

            }


class WageRequestForm(forms.Form):
    grower_no = forms.CharField(
        max_length=20, 
        label="Grower Number",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. G1234'})
    )
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        label="Amount ($)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason for charge/payment'}),
        label="Description"
    )

    # Validation: Check if the Grower actually exists
    def clean_grower_no(self):
        grower_no = self.cleaned_data.get('grower_no')
        if not Grower.objects.filter(grower_no=grower_no).exists():
            raise forms.ValidationError("Grower with this number does not exist.")
        return grower_no
