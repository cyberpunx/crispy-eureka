# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2021-01-27 20:25
from __future__ import unicode_literals

from django.db import migrations
import jsignature.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_auto_20210127_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='firma_entrada',
            field=jsignature.fields.JSignatureField(blank=True, null=True, verbose_name='Firma al entregar vehículo'),
        ),
        migrations.AddField(
            model_name='workorder',
            name='firma_salida',
            field=jsignature.fields.JSignatureField(blank=True, null=True, verbose_name='Firma al recibir vehículo'),
        ),
    ]
