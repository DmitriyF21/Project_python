from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio=models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="profile_pics", default='avatar.jpg')


def __str__(self):
    return f"{self.user},{self.profile.pic}"


