from django.conf import settings
from django.db import models

"""
member application 생성
    User 모델 구현
        username, nickname
    이후 해당 User모델을 Post나 Comment에서 author나 user 항목으로 참조
"""


# author, user 필드는 제외하고 생성

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    image = models.ImageField()

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PostLike',
        related_name='like_posts',
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', )

    def __str__(self):
        return '{}의 포스트'.format(self.author.username)

    @property
    def how_many_get_like(self):
        return self.post_like.count()

    def add_comment(self, user, content):
        return self.comment_set.create(
            author=user,
            content=content,
        )

    def add_tag(self, tag_name):
        tag, tag_created = Tag.objects.get_or_create(name=tag_name)
        if tag not in self.tags.filter(name=tag_name):
            self.tags.add(tag)


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


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    content = models.CharField(max_length=120)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CommentLike',
        related_name='like_comments'
    )

    def __str__(self):
        return '{}의 포스트에 대한 {}의 댓글 : {}'.format(
            self.post.author.username,
            self.author.username,
            self.content
        )


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
