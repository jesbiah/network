from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')


# Add additional models to this file to represent details about posts, likes, and followers. 
# Remember that each time you change anything in network/models.py, you’ll need to first run python manage.py makemigrations and then python manage.py migrate to migrate those changes to your database

class Post(models.Model):
    likes = models.ManyToManyField('User')
    text = models.CharField(max_length=256)
    timestamp = models.DateField(auto_now=True)
    posted_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')

