from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.
# Classes in Django represents Models

# We need a topic for room. SO lets create a mdoel for Topic


class Topic(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-update', '-created']


# Creating a model for messages
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # CASCADE means , if the room gets delted, delete all messages as well
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
    
    class Meta:
        ordering = ['-update', '-created']
