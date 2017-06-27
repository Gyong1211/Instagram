from django.conf import settings
from django.db import models

from utils.fields import CustomImageField

__all__ = (
    'Post',
    'PostLike'
)


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    image = CustomImageField(upload_to='post', blank=True)
    video = models.ForeignKey('Video', blank=True, null=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PostLike',
        related_name='like_posts',
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    my_comment = models.OneToOneField(
        'Comment',
        blank=True,
        null=True,
        related_name='+'
    )

    def __str__(self):
        return '{}의 포스트'.format(self.author.username)

    def add_comment(self, user, content):
        return self.comment_set.create(
            author=user,
            content=content,
        )

    @property
    def like_count(self):
        return self.like_users.count()

    class Meta:
        ordering = ['-pk', ]


class PostLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(auto_now_add=True)
