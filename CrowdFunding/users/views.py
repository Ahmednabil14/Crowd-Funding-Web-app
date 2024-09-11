from django.shortcuts import render, redirect
from .register_form import RegisterForm
from .login_form import LoginForm
from .models import User
from django.contrib.auth import authenticate, login

# Create your views here.

def Register(request):
    form = RegisterForm()
    context = {}
    context["form"] = form
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                email = form.cleaned_data["email"],
                password = form.cleaned_data["password"]
            )
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.phone = form.cleaned_data["phone"]
            user.profile_pic = form.cleaned_data["profile_pic"]
            user.save()
            return redirect("login")
        else:
            print(form.errors)

    return render(request, 'register.html', context=context)

def Login(request):
    form = LoginForm()
    context = {}
    context["form"] = form
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
            else:
                return render(request, 'login.html', context={"error": "Invalid username or password"})
        else:
            print(form.errors)
    return render(request, 'login.html', context=context)