# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 05:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0012_auto_20170623_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('d', 'Django'), ('f', 'Facebook')], default='d', max_length=1),
        ),
    ]
