import time
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from ..tasks import task_update_post_like_count
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
    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{}의 포스트'.format(self.author.username)

    def add_comment(self, user, content):
        return self.comment_set.create(
            author=user,
            content=content,
        )

    @property
    def comments(self):
        if self.my_comment:
            return self.comment_set.exclude(pk=self.my_comment.pk)
        return self.comment_set.all()

    def calc_like_count(self):
        time.sleep(1)
        self.like_count = self.like_users.count()
        self.save()

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

    class Meta:
        unique_together = (
            ('post', 'user')
        )


@receiver(post_save, sender=PostLike, dispatch_uid='postlike_save_update_like_count')
@receiver(post_delete, sender=PostLike, dispatch_uid='postlike_delete_update_like_count')
def update_post_like_count(sender, instance, **kwargs):
    if kwargs['signal'].receivers[0][0][0] == 'postlike_delete_update_like_count':
        instance.post.like_count -= 1
    else:
        instance.post.like_count += 1
    instance.post.save()
    print('Signal update_post_like_count, instance: {}'.format(
        instance
    ))
    task_update_post_like_count.delay(post_pk=instance.post.pk)
    print('LikeCount: {}'.format(instance.post.like_count))
