from django.shortcuts import render
from .register_form import RegisterForm

# Create your views here.

def Register(request):
    
    return render(request, 'register.html')