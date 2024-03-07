# Generated by Django 5.0.1 on 2024-03-07 13:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_posts_liked_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='liked_posts',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='liked_by',
        ),
        migrations.AddField(
            model_name='posts',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
