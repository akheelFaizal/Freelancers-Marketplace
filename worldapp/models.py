from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_freelancer = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Skill(models.Model):
    skill = models.CharField(unique=True, max_length=500)

    def __str__(self):
        return self.skill

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="userprofile")
    bio = models.TextField()
    skills = models.ManyToManyField(Skill)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    def __str__(self):
        return self.user.username

class Project(models.Model):
    client = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField()
    budget = models.DecimalField(max_digits=9, decimal_places=2)
    deadline = models.DateTimeField()
    is_open =models.BooleanField(default=True)

class Bid(models.Model):
    freelancer = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=9, decimal_places=2)
    message = models.TextField()
    created_at = models.DateTimeField

class Contract(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    freelancer = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    




