# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 00:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_class_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='alt_phone',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Telefono Alternativo'),
        ),
    ]
