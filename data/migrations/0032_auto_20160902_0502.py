# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-02 05:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0031_auto_20160831_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holding',
            name='metaData',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userHolding', to='data.HoldingMetaData'),
        ),
    ]