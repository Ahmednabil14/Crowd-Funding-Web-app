from django.db import models
from users.models import User

class Project(models.Model):

    title = models.CharField(max_length=255)
    details = models.TextField()
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    total_donations = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    project_pic = models.ImageField(upload_to="projects/images/profile_image", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def add_donation(self, amount):

        self.total_donations += amount
        self.save()

class Comment(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField(max_length=4000)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)