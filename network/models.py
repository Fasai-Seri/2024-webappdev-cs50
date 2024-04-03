from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, related_name='post', on_delete=models.CASCADE)
    content = models.TextField()
    posted_timestamp = models.DateTimeField()
    like_user = models.ManyToManyField(User, related_name='liked_post', blank=True)
    
    def __str__(self):
        return f'{self.posted_timestamp} by {self.poster}'
    
class FollowingRelationship(models.Model):
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relationship_followed')
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relationship_following')
    
    class Meta:
        unique_together = ('followed_user', 'following_user',)
        
    def __str__(self):
        return f'{self.followed_user} is followed by {self.following_user}'
