# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-26 13:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_timer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timer',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fin'),
        ),
        migrations.AlterField(
            model_name='timer',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 26, 10, 50, 0, 651001), verbose_name='Inicio'),
        ),
    ]
