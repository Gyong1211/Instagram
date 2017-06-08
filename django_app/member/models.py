from django.db import models

# Create your models here.
class User(models.model):
    name = models.CharField(max_length=40)
    nickname = models.CharField(max_length=40)