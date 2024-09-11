from django.shortcuts import render, redirect
from .register_form import RegisterForm
from .login_form import LoginForm
from .models import User
<<<<<<< HEAD
from django.contrib.auth import authenticate, login
=======
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
>>>>>>> dbb598143ea7f2a82e5e0ce2e689ce1c88e54443

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
<<<<<<< HEAD
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
=======
        user = RegisterForm(request.POST, request.FILES)
        if user.is_valid():
            user_instance = user.save(commit=False)  
            user_instance.is_active = False  
            user_instance.save()  
            send_activation_email(user_instance, request)
            messages.success(request, f'Dear {user_instance.first_name}, please go to your email inbox and click on the received activation link to confirm and complete the registration. Check your spam folder if necessary.')
            return redirect('login')
>>>>>>> dbb598143ea7f2a82e5e0ce2e689ce1c88e54443
        else:
            print(form.errors)

    return render(request, 'register.html', context=context)

def Login(request):
    form = LoginForm()
    context = {}
    context["form"] = form
    if request.method == "POST":
<<<<<<< HEAD
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
=======
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
>>>>>>> dbb598143ea7f2a82e5e0ce2e689ce1c88e54443
