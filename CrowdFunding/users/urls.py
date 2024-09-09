from django.urls import path
from .views import Register, Login

urlpatterns = [
    path('register', Register, name='register'),
    path('login', Login, name="login")
]