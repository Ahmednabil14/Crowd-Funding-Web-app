from django import forms
from users.models import User

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        label='First Name'
    )
    last_name = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        label='Last Name'
    )
    phone = forms.CharField(
        max_length=11, 
        min_length=11, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
        label='Mobile Phone'
    )
    profile_pic = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Profile Picture'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter a valid email'})
    )


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'password', 'password2', 'profile_pic')
