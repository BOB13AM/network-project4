from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name="user_followers")

    def count_followers(self):
        return self.followers.count()
    
    def count_following(self):
        return User.objects.filter(followers=self).count()
    
    def user_following(self):
        return User.objects.filter(followers=self)
    
    def serialize(self):
        return {
            "username": self.username,
            "email":self.email,
            "userid":self.id
        }
   

class post(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")
     body = models.TextField(blank=False)
     timestamp = models.DateTimeField(auto_now_add=True)
     user_likes = models.ManyToManyField(User, blank=True, related_name="user_like") 
     
     def count_likes(self):
        return self.user_likes.count()
     
     def serialize(self):
        likes = self.user_likes.count()   
        return {
            "id": self.id,
            "userid": self.user.id,
            "user": self.user.username,
            "body":self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "user_likes": [likes_user.username for likes_user in self.user_likes.all() ],
            "total_likes": likes
        }
