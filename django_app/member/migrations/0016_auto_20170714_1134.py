# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 02:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0015_auto_20170714_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
    ]
