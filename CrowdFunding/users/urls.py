from django.urls import path
from .views import Register, Login, activate, Logout, user_Info

urlpatterns = [
    path('register', Register, name='register'),
    path('login', Login, name="login"),
    path('userInfo', user_Info, name='user'),
    path('activate/<uidb64>/', activate, name='activate'),
    path('logout', Logout, name='logout')
]