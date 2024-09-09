from django.contrib.auth.forms import UserCreationForm
from django import forms
from users.models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    phone = forms.CharField(max_length=11, min_length=11)
    profile_pic = forms.FileField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone',
                  'password1', 'password2', 'profile_pic')