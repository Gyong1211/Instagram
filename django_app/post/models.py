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
        'member.User',
        on_delete=models.CASCADE
    )
    image = models.ImageField()
    content = models.TextField()
    tag = models.ManyToManyField(
        'Tag',
    )

    def __str__(self):
        return '{}의 포스트 : {}'.format(self.author.nickname, self.content)


class Comment(models.Model):
    author = models.ForeignKey(
        'member.User',
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    content = models.CharField(max_length=120)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}의 포스트 {}에 대한 {}의 댓글 : {}'.format(self.post.author.nickname, self.post.content, self.author.nickname, self.content)


class PostLike(models.Model):
    user = models.ForeignKey(
        'member.User',
    )
    like = models.PositiveIntegerField(default=0)


class Tag(models.Model):
    content=models.CharField(max_length=20)

    def __str__(self):
        return self.content