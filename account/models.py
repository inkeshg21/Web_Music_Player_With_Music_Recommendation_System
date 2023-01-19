from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to="static/user-images")
    phone = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.user

