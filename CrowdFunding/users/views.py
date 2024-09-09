from django.shortcuts import render, redirect
from .register_form import RegisterForm
from .login_form import LoginForm
from .models import User

# Create your views here.

def Register(request):
    form = RegisterForm()
    context = {}
    context["form"] = form
    if request.method == "POST":
        user = RegisterForm(request.POST, request.FILES)
        if user.is_valid():
            user.save()
            return redirect('login')
        else:
            print(user.errors)

    return render(request, 'register.html', context=context)

def Login(request):
    form = LoginForm()
    context = {}
    context["form"] = form
    if request.method == "POST":
        email = request.POST["email"]
        user = User.objects.get(email=email)
        print(user)
    return render(request, 'login.html', context=context)