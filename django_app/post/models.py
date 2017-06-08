from django.db import models

"""
member application 생성
    User 모델 구현
        username, nickname
    이후 해당 User모델을 Post나 Comment에서 author나 user 항목으로 참조
"""


# author, user 필드는 제외하고 생성

class Post(models.Model):
    image = models.ImageField()
    content = models.TextField()
    comment = models.ManyToManyField(
        'Comment',
        through='CommentInfo'
    )


class Comment(models.Model):
    content = models.TextField()


class PostLike(models.Model):
    like = models.PositiveIntegerField(default=0)


class Tag(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )


class CommentInfo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
