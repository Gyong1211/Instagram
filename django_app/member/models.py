from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q

"""
    동작
        follow : 내가 다른사람을 follow함
        unfollow : 내가 다른사람에게 한 follow를 취소함
    속성
        followers : 나를 follow하고 있는 사람들
        follower : 나를 follow하고 있는 사람
        following : 내가 follow하고 있는 사람들
        friend : 나와 서로 follow하고 있는 관계
        friends : 나와 서로 follow하고 있는 모든 관계
        없음 : 내가 follow하고 있는 사람 1명
            (나는 저 사람의 follower이다 또는 나는 저 사람을 follow하고 있다 라고 표현)
    ex) 내가 박보영, 최유정, 고성현을 follow하고 고성현과 김수정은 나를 follow한다
        나의 followers는 고성현, 김수정
        나의 following은 박보영, 최유정
        김수정은 나의 follower이다
        나는 박보영의 follower다
        나와 고성현은 friend관계이다
        나의 friends는 고성현 1명이다
"""


class User(AbstractUser):
    nickname = models.CharField(
        max_length=24,
        null=True,
        unique=True,
    )
    relations = models.ManyToManyField(
        'self',
        through='Relation',
        symmetrical=False,
    )

    def __str__(self):
        return self.nickname

    def follow_toggle(self, user):
        if not isinstance(user, User):
            raise ValueError
        # user를 팔로우하는 경우
        # to self from user 관계가 있는가?
        if self.from_self_relations.filter(to_user=user).exists():
            relation = self.from_self_relations.get(to_user=user)
            # 있으면 그게 블락인가?
            if relation.block:
                # 블락이라면 팔로우로 관계 변경 및 저장
                relation.block = False
                relation.save()
            #팔로우라면 관계 삭제
            else:
                relation.delete()
        #관계가 없는 경우
        else:
            #팔로우 관계 생성
            return self.from_self_relations.create(to_user=user, block=False)

    def is_follow(self, user):
        if not isinstance(user, User):
            raise ValueError

        return self.from_self_relations.filter(Q(to_user=user) & Q(block=False)).exists()

    def is_follower(self, user):
        if not isinstance(user, User):
            raise ValueError

        return self.to_self_relations.filter(Q(from_user=user) & Q(block=False)).exists()


    def block_toggle(self, user):
        if not isinstance(user, User):
            raise ValueError
        # user를 블락하는 경우
        # to self from user 관계가 있는가?
        if self.from_self_relations.filter(to_user=user).exists():

            relation = self.from_self_relations.get(to_user=user)
            # 있으면 그게 블락인가?
            if relation.block:
                # 블락이라면 블락 관계 삭제
                relation.delete()
            #팔로우라면 블락으로 관계 변경 후 세이브
            else:
                relation.block = True
                relation.save()
        #관계가 없는 경우
        else:
            #블락 관계 생성
            return self.from_self_relations.create(to_user=user, block=True)

    def is_block(self, user):
        if not isinstance(user, User):
            raise ValueError

        return self.from_self_relations.filter(Q(to_user=user) & Q(block=True)).exists()

    def is_blocked(self, user):
        if not isinstance(user, User):
            raise ValueError

        return self.to_self_relations.filter(Q(from_user=user) & Q(block=True)).exists()


    @property
    def following(self):
        relations = self.from_self_relations.filter(block=False)
        return User.objects.filter(pk__in=relations.values('to_user'))

    @property
    def followers(self):
        relations = self.to_self_relations.filter(block=False)
        return User.objects.filter(pk__in=relations.values('from_user'))

    @property
    def block(self):
        relations = self.from_self_relations.filter(block=True)
        return User.objects.filter(pk__in=relations.values('to_user'))

    @property
    def blocked(self):
        relations = self.to_self_relations.filter(block=True)
        return User.objects.filter(pk__in=relations.values('from_user'))


class Relation(models.Model):
    from_user = models.ForeignKey(
        User,
        related_name='from_self_relations',
    )
    to_user = models.ForeignKey(
        User,
        related_name='to_self_relations',
    )
    block = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Relation from {} to {} ({})'.format(
            self.from_user,
            self.to_user,
            'block' if self.block else 'follow',
        )

    class Meta:
        unique_together = (
            ('from_user', 'to_user')
        )
