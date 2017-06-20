import re

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
    image = models.ImageField(upload_to='post', blank=True)

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
    html_content = models.TextField(blank=True)
    tags = models.ManyToManyField('Tag')
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

    def save(self, *args, **kwargs):
        self.make_html_content_and_add_tags()
        super().save(*args, **kwargs)

    def make_html_content_and_add_tags(self):
        p = re.compile(r'(#\w+)')
        tag_name_list = re.findall(p, self.content)
        ori_content = self.content
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name.replace('#', ''))
            ori_content = ori_content.replace(
                tag_name,
                '<a href="#" class="hash-tag">{}</a>'.format(
                    tag_name
                )
            )
            if not self.tags.filter(pk=tag.pk).exists():
                self.tags.add(tag)
        self.html_content = ori_content


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
