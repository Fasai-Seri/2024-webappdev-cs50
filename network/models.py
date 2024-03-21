from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    following = models.ManyToManyField('self', related_name='followed')
    
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    poster = models.ForeignKey(User, related_name='post', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField()
    like_user = models.ManyToManyField(User, related_name='liked_post')
