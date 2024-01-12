from django.db import models
from django.contrib.auth.models import User

class Photo(models.Model):
    image = models.FileField(upload_to='photoStorage/')
    keywords = models.TextField(max_length=100)
    User = models.ForeignKey(User, on_delete=models.CASCADE)

class Album(models.Model):
    title = models.CharField(max_length=100)
    photos = models.ManyToManyField(Photo)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
