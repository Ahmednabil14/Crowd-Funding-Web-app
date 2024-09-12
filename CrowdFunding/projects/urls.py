from django.urls import path
from .views import create_project,edit_project,delete_project,show_project

urlpatterns = [
    path('create', create_project, name='create_project'),
    path('edit/<int:id>', edit_project, name='edit_project'),
    path('delete/<int:id>',delete_project,name='delete_project'),
    path('show/<int:id>',show_project,name='show_project')

]