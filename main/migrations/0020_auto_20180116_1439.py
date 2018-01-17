# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-16 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20180116_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='total_manual',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total'),
        ),
        migrations.AlterField(
            model_name='workorderparts',
            name='price',
            field=models.FloatField(blank=True, verbose_name='Precio'),
        ),
        migrations.AlterField(
            model_name='workorderparts',
            name='quantity',
            field=models.IntegerField(blank=True, default=1, verbose_name='Cantidad'),
        ),
        migrations.AlterField(
            model_name='workorderworks',
            name='time_required',
            field=models.IntegerField(blank=True, default=1, verbose_name='Tiempo'),
        ),
    ]