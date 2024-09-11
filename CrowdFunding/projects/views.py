from django.shortcuts import render, redirect
from .form import ProjectForm
from .models import Project

# Create your views here.


def create_project(request):
    context = {}
    form = ProjectForm()
    context["form"] = form
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            print(form)
            form.save()
            return redirect("home")
    return render(request, 'create_project.html', context=context)

def home(request):
    return render(request, 'home.html')