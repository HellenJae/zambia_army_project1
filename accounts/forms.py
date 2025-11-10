# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

UNIT_CHOICES = [
    ('', 'Select Unit'),
    ('engineering', 'Engineering'),
    ('logistics', 'Logistics'),
    ('infantry', 'Infantry'),
    ('commando', 'Commando'), 
    # add more units here
]

ROLE_CHOICES = [
    ('', 'Select Role'),
    ('soldier', 'Soldier'),
    ('officer', 'Officer'),
    ('commander', 'Commander'),
    ('admin', 'Admin'),

]

class CustomUserCreationForm(UserCreationForm):
    man_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Man Number'})
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    unit = forms.ChoiceField(
        choices=UNIT_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = CustomUser
        fields = ['man_number', 'first_name', 'last_name', 'unit', 'role', 'password1', 'password2']
 