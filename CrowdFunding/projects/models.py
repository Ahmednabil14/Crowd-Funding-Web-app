from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):

    name = models.CharField(max_length=100, unique=True, db_column='category_name')

    def __str__(self):
        return self.name

class Project(models.Model):

    title = models.CharField(max_length=255, db_column='project_title')
    details = models.TextField(db_column="project_details")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, db_column='category_id')
    multiple_pics = models.ManyToManyField('Picture', blank=True, related_name='projects', db_column='pictures')
    total_target = models.DecimalField(max_digits=10, decimal_places=2, db_column="target_amount")
    total_donations = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, db_column="total_donations")
    multiple_tags = models.ManyToManyField('Tag', blank=True, related_name='projects', db_column='tags')
    start_time = models.DateTimeField(auto_now_add=True, db_column='campaign_start_time')
    end_time = models.DateTimeField(db_column="campaign_end_time")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', db_column='creator_id')
    is_active = models.BooleanField(default=True, db_column='is_active')
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, db_column='average_rating')
    total_ratings = models.PositiveIntegerField(default=0, db_column='total_ratings')

    def __str__(self):
        return self.title

    def add_donation(self, amount):

        self.total_donations += amount
        self.save()
    def add_rating(self, new_rating):
    
        total_score = self.average_rating * self.total_ratings
        self.total_ratings += 1
        self.average_rating = (total_score + new_rating) / self.total_ratings
        self.save()

class Picture(models.Model):

    image = models.ImageField(upload_to='project_pics/', db_column='image_file')
    description = models.CharField(max_length=255, blank=True, db_column='image_description')

    def __str__(self):
        return self.description or 'No description'

class Tag(models.Model):

    name = models.CharField(max_length=50, blank=True, db_column='tag_name')

    def __str__(self):
        return self.name

class Comment(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments', db_column="project_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', db_column='user_id')
    text = models.TextField(max_length=1000, db_column='comment_text')
    created_at = models.DateTimeField(auto_now_add=True, db_column='comment_created_at')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', db_column='parent_comment')

    def __str__(self):
        return f'Comment by {self.user} on {self.project}'


class Report(models.Model):

    REPORT_TYPE_CHOICES = [
        ('project', 'Project'),
        ('comment', 'Comment'),
    ]
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES, db_column="report_type")
    content_id = models.PositiveIntegerField(db_column="reported_content_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="reporting_user_id")
    reason = models.TextField(max_length=500, db_column="report_reason")

    def __str__(self):
        return f'Report by {self.user} on {self.report_type} {self.content_id}'

