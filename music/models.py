from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Music(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    file = models.FileField(upload_to="static/music")
    cover = models.ImageField(upload_to="static/images")
    poster = models.ImageField(upload_to="static/images")
    duration = models.CharField(max_length=50)
    genre = models.CharField(max_length=250)
    singer = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
