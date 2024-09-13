from django.shortcuts import render, redirect,get_object_or_404
from .form import ProjectForm , CommentForm
from .models import Project, Comment,Rating
from decimal import Decimal
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from django.http import HttpResponseRedirect
# Create your views here.


def create_project(request):
    if request.user.is_authenticated:
        context = {}
        form = ProjectForm()
        context["form"] = form
        if request.method == "POST":
            form = ProjectForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                tags = form.cleaned_data['tags']
                del data['tags']
                project = Project.objects.create(user=request.user, **data)
                project.tags.set(tags)
                return redirect("home")
    else:
        return redirect('login')
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
        else:
            messages.warning(request, "Project cannot be deleted as Donations are more than 25%")
            return redirect('show_project',id=id)


def home(request):
    context = {}
    projects = Project.objects.all()
    context["projects"] = projects
    return render(request, 'home.html', context)

def show_project(request, id):
    project = get_object_or_404(Project, pk=id)
    comments = project.comments.filter(active=True)
    new_comment = None
    comment_form=None
    rating=None

    if request.method == "POST":
        # Handle donation
        amount = Decimal(request.POST.get('amount', '0'))
        if amount > 0:
            project.add_donation(amount, request.user)
            messages.success(request, f'Thank you for your contribution of {amount}.')
        else:
            messages.error(request, 'Invalid donation amount.')

        # Handle comment submission
        if request.user.is_authenticated:

            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = Comment.objects.create(project=project, user=request.user,
                                    comment=comment_form.cleaned_data.get('comment'), active=True)
                messages.success(request, 'Your comment has been posted.')
                comments = project.comments.filter(active=True)
            else:
                messages.error(request, 'There was an error with your comment.')
        else:
                messages.error(request, 'Please Login First')

        
 # Handle rating submission
        if 'rating' in request.POST:
            rating_value = request.POST.get('rating')
            if rating_value:
                if request.user.is_authenticated:
                    rating_value = int(rating_value)
                    rating, created = Rating.objects.get_or_create(
                        project=project,
                        user=request.user,
                        defaults={'value': rating_value}
                    )
                    if not created:
                        rating.value = rating_value
                        rating.save()
                    project.update_average_rating()
                    messages.success(request, 'Your rating has been submitted.')
                else:
                    messages.warning(request, 'Please Login First')
    else:
        comment_form = CommentForm()

        if request.user.is_authenticated:
            rating = Rating.objects.filter(project=project, user=request.user).first()
        else:
            rating = None
    
    user_donation = project.get_user_donations(request.user)
    print(f"You have donated {user_donation} to this project.")
    context = {
        'project': project,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'rating': rating,
        'user_donation': user_donation 
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
