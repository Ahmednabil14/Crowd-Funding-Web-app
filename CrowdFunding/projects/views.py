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
            Project.objects.create(user=request.user, **form.cleaned_data)
            return redirect("home")
    return render(request, 'create_project.html', context=context)

def home(request):
    context = {}
    projects = Project.objects.all()
    context["projects"] = projects
    return render(request, 'home.html', context)