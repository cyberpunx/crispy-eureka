# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 21:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20170713_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='date_in',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha Entrada'),
        ),
        migrations.AddField(
            model_name='workorder',
            name='date_out',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha Salida'),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='status',
            field=models.CharField(choices=[('PRE', 'Presupuesto'), ('REV', 'Revisión Inicial'), ('ING', 'Esperando Ingreso'), ('ABI', 'Abierta'), ('INI', 'Iniciada'), ('REP', 'Esperando repuestos'), ('PAU', 'Pausada'), ('RET', 'Esperando Retiro'), ('COM', 'Completa'), ('CER', 'Cerrada'), ('CAN', 'Cancelada')], max_length=3, verbose_name='Estado'),
        ),
    ]
