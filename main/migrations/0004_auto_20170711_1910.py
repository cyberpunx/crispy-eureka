# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 19:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20170711_1902'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workorder',
            options={'permissions': [('can_edit_workorder_settings', 'Can edit work order settings')]},
        ),
    ]
