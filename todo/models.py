from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Project(models.Model):
    name         = models.CharField(max_length=30, unique=True)
    description  = models.CharField(max_length=100)
    favourite    = models.BooleanField(default=False)
    created_by   = models.ForeignKey(User,null=True,related_name='project',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Outline(models.Model):
    name = models.CharField(max_length=50)
    deadline = models.DateField(null=True)    
    status = models.BooleanField(default=False) 
    created_by = models.ForeignKey(User,null=True,related_name='projects',on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='outlines',on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=100)
    deadline = models.DateTimeField(null=True)
    PRO = (
            (1, 'Urgent'),
            (2, 'Important'),
            (3, 'Moderate'),
            (4, 'Not Important')
        )
    priority = models.IntegerField(choices=PRO, default=4)
    created_by = models.ForeignKey(User,null=True,related_name='tasks',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at  = models.DateTimeField(null=True)
    status = models.BooleanField(default=False)
    outline = models.ForeignKey(Outline,null=True,related_name='tasks',on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio  = models.TextField(max_length=100, blank=True)
    image = models.ImageField(upload_to='static/media/',default = 'static/media/profile.jpg')

    def __str__(self):
        return self.bio

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()





