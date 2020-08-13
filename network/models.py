from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass

class Following(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="follower")
    following = models.ManyToManyField(User, blank=True, related_name="following")
    followers = models.ManyToManyField(User, blank=True, related_name="followers")

class Like(models.Model):
    users = models.ManyToManyField(User, related_name="like_users")
    num = models.PositiveIntegerField(default=0)

class Comment(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete = models.CASCADE, related_name="comment_user")
    comment = models.TextField()

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        exclude = ('user',)
        labels = {
            "comment": _("Comment"),
        }
        widgets = {
            "message": Textarea(
                attrs={"rows": 5, "cols": 200}
            )
        }
        error_messages = {
            'text': {
                'max_length': _("This comment is too long."),
            },
        }

class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="post_user")
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    likes = models.ForeignKey(Like, null=True, blank=True, on_delete = models.CASCADE, related_name="post_likes")
    comments = models.ManyToManyField(Comment, blank=True, related_name="post_comments")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "text": self.text,
            "time": self.time.strftime("%B %d, %Y, %I:%M %p"),
            "likes": self.likes.num,
            "comments": [c.comment for c in self.comments.all()],
        }

class PostForm(ModelForm):
    class Meta: 
        model = Post
        fields = ('text',)
        exclude = ('user','time','likes','comments',)
        widgets = {
            "message": Textarea(
                attrs={"rows": 5, "cols": 200}
            )
        }
        error_messages = {
            'text': {
                'max_length': _("This post is too long."),
            },
        }