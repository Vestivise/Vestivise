# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-04 21:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0027_auto_20170104_0232'),
    ]

    operations = [
        migrations.AddField(
            model_name='holding',
            name='mstarid',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
