# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-27 07:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0023_auto_20161224_0630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='averageusersharpe',
            name='mean',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='averageusersharpe',
            name='std',
            field=models.FloatField(null=True),
        ),
    ]
