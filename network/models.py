from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def get_following_list(self):
        """Return a list of following user objects"""
        return [following.following_user for following in self.following.all()]

    def get_followers_list(self):
        """Return a list of followers user objects"""
        return [follower.user for follower in self.followers.all()]


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


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_posts")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user} likes Post {self.post.id}"


class UserFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "following_user")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user} follows {self.following_user}"
