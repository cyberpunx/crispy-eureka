# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2021-01-28 02:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0051_auto_20210127_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='vehicle_model',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Modelo'),
        ),
    ]
