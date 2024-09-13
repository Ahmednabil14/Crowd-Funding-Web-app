from django import forms
from users.models import User
import pycountry

class UpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        label='First Name',
        required=False
    )
    last_name = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        label='Last Name',
        required=False
    )
    phone = forms.CharField(
        max_length=11, 
        min_length=11, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
        label='Mobile Phone',
        required=False
    )
    profile_pic = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Profile Picture',
        required=False
    )

    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Birth Date',
        required=False
    )

    facebook_profile = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Facebook Profile'}),
        label='Facebook Profile',
        required=False
        )

    country_choices = [(country.name, country.name) for country in pycountry.countries]

    country = forms.ChoiceField(
        choices=country_choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Country',
        required=False
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone',
                  'profile_pic', 'birth_date', 'facebook_profile', 'country')
