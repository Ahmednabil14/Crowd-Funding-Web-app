from django import forms
from projects.models import Project , Comment, Tag

class ProjectForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
        label='Title'
    )
    details = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        label='Description'
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Tags'
    )

    total_target = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Target'}),
        label='Target'
    )
    project_pic = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Project Picture'
    )

    end_time = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}),
        label='End Date'
    )



    class Meta:
        model = Project
        fields = ('title', 'details', 'tags', 'total_target', 'project_pic', 'end_time')
    

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comment'}),
        label='Comment'
    )
    class Meta:
        model = Comment
        fields = ('comment',)
