# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-12 14:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20180112_1108'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=40, verbose_name='Categoría')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripción')),
            ],
        ),
        migrations.RenameModel(
            old_name='Category',
            new_name='PartCategory',
        ),
        migrations.AlterField(
            model_name='work',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='main.WorkCategory', verbose_name='Categoría'),
        ),
    ]