from django.db import models
from users.models import User
from django.db.models import JSONField,Avg 

class Category(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category
    
    

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):

    title = models.CharField(max_length=255)
    details = models.TextField()
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    total_donations = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tags = models.ManyToManyField(Tag)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateField()
    project_pic = models.ImageField(upload_to="projects/images/profile_image", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    donations = JSONField(default=dict)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    def add_donation(self, amount, user):

        self.total_donations += amount

        user_id = str(user.id)  

        if user_id in self.donations:
            self.donations[user_id] += float(amount)
        else:
            self.donations[user_id] = float(amount)

        self.save()
    def get_user_donations(self, user):
        user_id = str(user.id)
        return self.donations.get(user_id, 0)
    
    def update_average_rating(self):
        avg_rating = self.ratings.aggregate(Avg('value'))['value__avg']
        if avg_rating is not None:
            self.average_rating = avg_rating
        else:
            self.average_rating = 0.00
        self.save()

class ProjectReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Comment(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=4000)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


class Rating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)]) 

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return f'{self.value} stars for {self.project.title}'
    
