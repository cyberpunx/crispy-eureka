# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-01 22:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_auto_20180301_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movement',
            name='date',
            field=models.DateField(blank=True, verbose_name='Fecha'),
        ),
    ]
