# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-17 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20180117_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='kilometers',
            field=models.IntegerField(blank=True, null=True, verbose_name='Kilometraje'),
        ),
    ]