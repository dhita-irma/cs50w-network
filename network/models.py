from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.TextField(max_length=240)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    # likes = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="liked")

    def __str__(self):
        return f"{self.creator} - {self.content}"

    # Return JSON representation of the email
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "creator": self.creator.username,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }

class UserFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "following_user")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user} follows {self.following_user}"

    def serialize(self):
        return {
            "user": self.user.username,
            "following": self.following_user.username
        }