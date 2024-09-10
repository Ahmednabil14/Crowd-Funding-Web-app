from django.shortcuts import render, redirect
from .register_form import RegisterForm
from .login_form import LoginForm
from .models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages

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
        user = RegisterForm(request.POST, request.FILES)
        if user.is_valid():
            user_instance = user.save(commit=False)  
            user_instance.is_active = False  
            user_instance.save()  
            send_activation_email(user_instance, request)
            messages.success(request, f'Dear {user_instance.first_name}, please go to your email inbox and click on the received activation link to confirm and complete the registration. Check your spam folder if necessary.')
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