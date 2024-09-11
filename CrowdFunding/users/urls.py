from django.urls import path
from .views import Register, Login, activate, Logout

urlpatterns = [
    path('register', Register, name='register'),
    path('login', Login, name="login"),
    path('activate/<uidb64>/', activate, name='activate'),
    path('logout', Logout, name='logout')
]