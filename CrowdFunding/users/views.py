from django.shortcuts import render, redirect
from .register_form import RegisterForm
from .login_form import LoginForm
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from projects.models import Project
from .update_form import *
# Create your views here.

def send_activation_email(user, request):
    subject = "Activate your account"
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = f"http://{request.get_host()}/user/activate/{uid}/"
    message = f"Hello {user.first_name}, please click the link to activate your account: {activation_link}"

    send_mail(
        subject,
        message,
        'an63805@gmail.com',  
        [user.email],  
        fail_silently=False,
    )

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
            user.is_active = False  
            send_activation_email(user, request)
            messages.success(request, f'Dear {user.first_name}, please go to your email inbox and click on the received activation link to confirm and complete the registration. Check your spam folder if necessary.')
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
                return redirect("home")
            else:
                return render(request, 'login.html', context={"error": "Invalid username or password"})
        else:
            print(form.errors)
    return render(request, 'login.html', context=context)

def activate(request, uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user.is_active = True
        user.save()
        messages.success(request, 'Account activated successfully! You can now log in.')
        return redirect('login')
    except User.DoesNotExist:
        messages.error(request, 'Invalid activation link')
        return redirect('register')
    


def user_Info(request):
    if not request.user.is_authenticated:
        return redirect('login')
    projects_with_donations = Project.objects.filter(donations__has_key=str(request.user.id))
    user_projects=Project.objects.filter(user=request.user)

    user_donations = []
    for project in projects_with_donations:
        donation_amount = project.get_user_donations(request.user)
        user_donations.append({
            'project': project,
            'donation_amount': donation_amount
        })


    return render(request, 'user.html', {'user': request.user,  'user_donations': user_donations,'user_projects': user_projects})


def delete_user(request):
    if request.method == "POST":
        request.user.delete()
        return redirect('login')
    else:
        return render(request, 'delete_user.html')



def update(request):
    context = {}
    form = UpdateForm(instance=request.user)
    context["form"] = form
    if request.method == "POST":
        form = UpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            update_data = {}
            for key, value in form.cleaned_data.items():
                if value:
                    update_data[key] = value
            User.objects.filter(id=request.user.id).update(**update_data)
            return redirect('user')
    return render(request, "update.html", context)


def Logout(request):
    logout(request)
    return redirect('login')