# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-09 06:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
        ('post', '0003_auto_20170608_2104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postlike',
            name='like',
        ),
        migrations.AddField(
            model_name='post',
            name='post_like',
            field=models.ManyToManyField(related_name='post_like', through='post.PostLike', to='member.User'),
        ),
        migrations.AddField(
            model_name='postlike',
            name='post',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='post.Post'),
            preserve_default=False,
        ),
    ]
