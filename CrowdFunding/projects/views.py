from django.shortcuts import render, redirect,get_object_or_404
from .form import ProjectForm , CommentForm
from .models import Project, Comment
from decimal import Decimal
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from django.http import HttpResponseRedirect
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

def show_project(request, id):
    project = get_object_or_404(Project, pk=id)
    comments = project.comments.filter(active=True)
    new_comment = None

    if request.method == "POST":
        # Handle donation
        amount = Decimal(request.POST.get('amount', '0'))
        if amount > 0:
            project.add_donation(amount)
            messages.success(request, f'Thank you for your contribution of {amount}.')
        else:
            messages.error(request, 'Invalid donation amount.')

        # Handle comment submission
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = Comment.objects.create(project=project, user=request.user,
                                   comment=comment_form.cleaned_data.get('comment'), active=True)
            messages.success(request, 'Your comment has been posted.')
            comments = project.comments.filter(active=True)
        else:
            messages.error(request, 'There was an error with your comment.')
    else:
        comment_form = CommentForm()

    context = {
        'project': project,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    
    return render(request, 'show_project.html', context)

class SearchResultsView(ListView):
    model = Project
    template_name = 'search_result.html'
    context_object_name = 'projects'
    def get_queryset(self):  
        query = self.request.GET.get("q")
        print("Search query:", query) 
        object_list = Project.objects.filter(
            Q(title__icontains=query)
        )
        return object_list
