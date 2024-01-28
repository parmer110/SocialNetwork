from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

class Follow(models.Model):
    id = models.AutoField(primary_key=True)
    userPointer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    userTarget = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed", null=True)
    timestamp = models.DateTimeField(auto_now=True)

class FollowChange(models.Model):
    id = models.AutoField(primary_key=True)
    follow = models.ForeignKey(Follow, on_delete=models.CASCADE, related_name="followChange")
    followUnfollow = models.BooleanField()
    timestamp = models.DateTimeField()

class Like(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="userLikes")
    timestamp = models.DateTimeField(auto_now=True)
    likeUnlike = models.BooleanField(default=False)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes', null=True)

    def __str__(self):
        return f"{self.likeUnlike}"

class LikeChange(models.Model):
    id = models.AutoField(primary_key=True)
    like = models.ForeignKey(Like, models.CASCADE, related_name="likeChange")
    likeUnlike = models.BooleanField(default=False)
    timestamp = models.DateTimeField()
    
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=4096)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="userPosts")

    class Meta:
        ordering = ('timestamp', )

    def __str__(self):
        return f"{self.id}- {self.user}, {self.timestamp}"

class PostEdition(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="revisions")
    content = models.TextField(max_length=4096)
    timestamp = models.DateTimeField()

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="comment")
    content = models.TextField(max_length=4096)
    timestamp = models.DateTimeField(auto_now=True)

class CommentChange(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="change")
    content = models.TextField(max_length=4096)
    timestamp = models.DateTimeField()