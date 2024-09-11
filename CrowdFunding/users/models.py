from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class ManagerUser(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError(("The Email must be set"))
        if not password:
            raise ValueError(("The password must be set"))
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    last_login = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=11, validators=[MinLengthValidator(11)])
    profile_pic = models.FileField(upload_to="users/images", null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    facebook_profile = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = ManagerUser()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["password"]

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True