# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2021-01-28 20:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0053_vehicle_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timer',
            name='start_time',
            field=models.DateTimeField(verbose_name='Inicio'),
        ),
    ]