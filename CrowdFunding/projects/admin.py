from django.contrib import admin
from projects.models import Project , Comment, Category
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'project', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('user', 'comment')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

# admin.site.register(Tag)

admin.site.register(Project)   
admin.site.register(Category) 