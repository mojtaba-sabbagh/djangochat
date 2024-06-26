from django.contrib.auth.models import User
from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    opened = models.BooleanField(default=False)
    nikname = models.CharField(max_length=255, default='Guest')

    def __str__(self):
        return f"{self.name} - {self.nikname}"  # This is just an example, customize as needed

class MessageIntegerChoices(models.IntegerChoices):
    MESSAGE = 1
    FILE = 2

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    kind = models.IntegerField(choices=MessageIntegerChoices.choices, default=1)
    def __str__(self):
        return f"{self.content} --- {self.room}"  # This is just an example, customize as needed
    class Meta:
        ordering = ('date_added',)