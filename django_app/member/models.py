import re

import requests
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from django.db.models import Q
from django.conf import settings

from utils.fields import CustomImageField

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


class UserManager(DefaultUserManager):
    def get_or_create_facebook_user(self, user_info):
        username = '{}_{}_{}'.format(
            self.model.USER_TYPE_FACEBOOK,
            settings.FACEBOOK_APP_ID,
            user_info['id']
        )
        user, user_created = self.get_or_create(
            username=username,
            user_type=self.model.USER_TYPE_FACEBOOK,
            defaults={
                'last_name': user_info.get('last_name', ''),
                'first_name': user_info.get('first_name', ''),
                'email': user_info.get('email', ''),
            }
        )
        if user_created and user_info.get('picture'):
            url_picture = user_info['picture']['data']['url']
            p = re.compile(r'.*\.([^?]+)')
            file_ext = re.search(p, url_picture).group(1)
            file_name = '{}.{}'.format(
                user.pk,
                file_ext
            )

            temp_file = NamedTemporaryFile()

            response = requests.get(url_picture)

            temp_file.write(response.content)

            user.img_profile.save(file_name, File(temp_file))

        return user


class User(AbstractUser):
    USER_TYPE_DJANGO = 'd'
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_CHOICES = (
        (USER_TYPE_DJANGO, 'Django'),
        (USER_TYPE_FACEBOOK, 'Facebook'),
    )
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default=USER_TYPE_DJANGO)
    nickname = models.CharField(
        max_length=24,
        null=True,
        unique=True,
    )
    img_profile = CustomImageField(
        upload_to='member',
        blank=True,
        default_static_image='images/profile.png'
    )
    relations = models.ManyToManyField(
        'self',
        through='Relation',
        symmetrical=False,
    )
    email = models.EmailField(null=True, unique=True)
    objects = UserManager()

    def __str__(self):
        return self.username

    def follow(self, user):
        if not isinstance(user, User):
            raise ValueError('"user" argument must <User> class')
        if self.from_self_relations.filter(to_user=user).exists():
            relation = self.from_self_relations.get(to_user=user)
            # 있으면 그게 블락인가?
            if relation.relation_type == 'bl':
                # 블락이라면 팔로우로 관계 변경 및 저장
                relation.relation_type = 'fl'
                relation.save()
            else:
                pass
        else:
            self.from_self_relations.create(
                to_user=user,
                relation_type='fl'
            )


    def unfollow(self, user):
        Relation.objects.filter(
            from_user=self,
            to_user=user,
            relation_type='fl'
        ).delete()

    def follow_toggle(self, user):
        if not isinstance(user, User):
            raise ValueError
        # user를 팔로우하는 경우
        # to self from user 관계가 있는가?
        if self.from_self_relations.filter(to_user=user).exists():
            relation = self.from_self_relations.get(to_user=user)
            # 있으면 그게 블락인가?
            if relation.relation_type == 'bl':
                # 블락이라면 팔로우로 관계 변경 및 저장
                relation.relation_type = 'fl'
                relation.save()
            # 팔로우라면 관계 삭제
            else:
                relation.delete()
        # 관계가 없는 경우
        else:
            # 팔로우 관계 생성
            return self.from_self_relations.create(to_user=user, relation_type='fl')

    def is_follow(self, user):
        if not isinstance(user, User):
            raise ValueError

        return self.from_self_relations.filter(Q(to_user=user) & Q(relation_type='fl')).exists()

    def is_follower(self, user):
        if not isinstance(user, User):
            raise ValueError

        return self.to_self_relations.filter(Q(from_user=user) & Q(relation_type='fl')).exists()

    def block_toggle(self, user):
        if not isinstance(user, User):
            raise ValueError
        # user를 블락하는 경우
        # to self from user 관계가 있는가?
        if self.from_self_relations.filter(to_user=user).exists():

            relation = self.from_self_relations.get(to_user=user)
            # 있으면 그게 블락인가?
            if relation.relation_type == 'bl':
                # 블락이라면 블락 관계 삭제
                relation.delete()
            # 팔로우라면 블락으로 관계 변경 후 세이브
            else:
                relation.relation_type = 'bl'
                relation.save()
        # 관계가 없는 경우
        else:
            # 블락 관계 생성
            return self.from_self_relations.create(to_user=user, relation_type='bl')

    def is_block(self, user):
        if not isinstance(user, User):
            raise ValueError

        return self.from_self_relations.filter(Q(to_user=user) & Q(relation_type='bl')).exists()

    def is_blocked(self, user):
        if not isinstance(user, User):
            raise ValueError

        return self.to_self_relations.filter(Q(from_user=user) & Q(relation_type='bl')).exists()

    @property
    def following(self):
        relations = self.from_self_relations.filter(relation_type='fl')
        return User.objects.filter(pk__in=relations.values('to_user'))

    @property
    def followers(self):
        relations = self.to_self_relations.filter(relation_type='fl')
        return User.objects.filter(pk__in=relations.values('from_user'))

    @property
    def block(self):
        relations = self.from_self_relations.filter(relation_type='bl')
        return User.objects.filter(pk__in=relations.values('to_user'))

    @property
    def blocked(self):
        relations = self.to_self_relations.filter(relation_type='bl')
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
    types_of_relation = (
        ('fl', 'follow'),
        ('bl', 'block'),
    )
    relation_type = models.CharField(
        max_length=2,
        choices=types_of_relation
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Relation from {} to {} ({})'.format(
            self.from_user,
            self.to_user,
            self.relation_type,
        )

    class Meta:
        unique_together = (
            ('from_user', 'to_user')
        )
