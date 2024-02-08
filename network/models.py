from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
    username = models.ForeignKey('User', null=True, on_delete=models.SET_NULL)
    post_content = models.CharField(max_length=1000)
    creation_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    likes = models.IntegerField(default=0)

class Comments(models.Model):
    username = models.ForeignKey('User', null=True, on_delete=models.SET_NULL)
    related_post = models.ForeignKey('Posts', on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)