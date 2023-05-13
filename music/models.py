from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Artist(models.Model):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to="static/artist-images")
    country = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=10, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)


class Music(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    file = models.FileField(upload_to="static/music")
    cover = models.ImageField(upload_to="static/images")
    poster = models.ImageField(upload_to="static/images")
    duration = models.CharField(max_length=50)
    genre = models.CharField(max_length=250)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)


class Playlist(models.Model):
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)


class History(models.Model):
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Music, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=1000, null=True)
