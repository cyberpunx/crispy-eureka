# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2021-01-28 22:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0054_auto_20210128_1749'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workorder',
            options={},
        ),
        migrations.AddField(
            model_name='workorderworks',
            name='work_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Sobreescribir Total'),
        ),
    ]
