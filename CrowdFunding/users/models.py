from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=11, validators=[MinLengthValidator(11)])
    profile_pic = models.FileField(upload_to="users/images")
    birth_date = models.DateField(null=True)
    facebook_profile = models.TextField(null=True)
    country = models.CharField(max_length=30,null=True)

    USERNAME_FIELD = 'email'
