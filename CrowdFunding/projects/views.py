from django.shortcuts import render, redirect,get_object_or_404
from .form import ProjectForm
from .models import Project
from decimal import Decimal
from django.contrib import messages

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

def edit_project(request,id):
    project = get_object_or_404(Project, pk=id)
    if request.user != project.user:
        messages.error(request, "Permission Denied")
        return render(request,'rejected.html')
    context = {}
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'edit_project.html')
    form = ProjectForm(instance=project)
    context = {'form': form}
    return render(request, 'edit_project.html', context=context)

def delete_project(request,id):
    project = get_object_or_404(Project, pk=id)
    if request.user != project.user:
        messages.error(request, "Permission Denied")
        return render(request,'rejected.html')
    if request.method == 'POST':
        if project.total_donations < project.total_target * Decimal(0.25):
            project.delete()
            return redirect('home')

def home(request):
    context = {}
    projects = Project.objects.all()
    context["projects"] = projects
    return render(request, 'home.html', context)

def show_project(request,id):
    project = get_object_or_404(Project, pk=id)
    context={"project" :project}
    return render(request,'show_project.html',context=context)