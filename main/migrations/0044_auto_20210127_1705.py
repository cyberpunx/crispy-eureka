# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2021-01-27 20:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0043_auto_20210127_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timer',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 27, 17, 5, 49, 184299), verbose_name='Inicio'),
        ),
    ]