from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser, models.Model):
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    follower_list = models.ManyToManyField('User', blank=True, related_name='followers')
    following_list = models.ManyToManyField('User', blank=True, related_name='following')
    liked_posts = models.ForeignKey('Posts', null=True, on_delete=models.CASCADE)

class Posts(models.Model):
    username = models.ForeignKey('User', null=True, on_delete=models.SET_NULL, related_name='all_posts')
    post_content = models.CharField(max_length=1000)
    creation_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    likes = models.IntegerField(default=0)

class Comments(models.Model):
    username = models.ForeignKey('User', null=True, on_delete=models.SET_NULL)
    related_post = models.ForeignKey('Posts', on_delete=models.CASCADE, related_name='all_comments')
    content = models.CharField(max_length=1000)