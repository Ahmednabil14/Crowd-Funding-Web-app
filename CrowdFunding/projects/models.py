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

