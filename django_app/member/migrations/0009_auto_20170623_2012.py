# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-23 11:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0008_auto_20170623_1426'),
    ]

    operations = [
        migrations.RenameField(
            model_name='relation',
            old_name='block',
            new_name='type',
        ),
    ]
