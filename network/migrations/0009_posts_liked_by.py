# Generated by Django 5.0.1 on 2024-03-07 13:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_user_liked_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='liked_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
