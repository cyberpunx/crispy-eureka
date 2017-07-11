# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 06:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='Employee',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='main.Employee', verbose_name='Empleado'),
        ),
        migrations.AddField(
            model_name='workorder',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='subcategory_name',
            field=models.CharField(max_length=40, verbose_name='Subcategoría'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='status',
            field=models.CharField(choices=[('PRE', 'Presupuesto'), ('ABI', 'Abierta'), ('PRO', 'En Progreso'), ('PAU', 'Pausada'), ('COM', 'Completa'), ('CER', 'Cerrada'), ('CAN', 'Cancelada')], max_length=3, verbose_name='Estado'),
        ),
    ]