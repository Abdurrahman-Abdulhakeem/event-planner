from django.db import models
from django.shortcuts import reverse

from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, default="empty_logo.png")
    followers = models.ManyToManyField('self', symmetrical=False, blank=True)
    following = models.ManyToManyField('self', related_name='user_following', symmetrical=False, blank=True)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username or self.full_name.split()[0]
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.username, 'id': self.id})
    

class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name='members', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'id': self.id})
    
    def get_edit_url(self):
        return reverse('edit-event', kwargs={'id': self.id})
    
    def get_delete_url(self):
        return reverse('event-delete', kwargs={'id': self.id})
    
    def __str__(self):
        return self.name
    
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']
        
    def get_delete_url(self):
        return reverse('message-delete', kwargs={'id': self.id})
    
    def __str__(self):
        return self.body[:10]