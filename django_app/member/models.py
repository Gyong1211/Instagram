from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField(
        max_length=24,
        null=True,
        unique=True,
    )

    # def __str__(self):
    #     return self.nickname