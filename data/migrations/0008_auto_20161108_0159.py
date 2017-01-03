# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-08 01:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_auto_20161105_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='holding',
            name='currentUpdateIndex',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='holdingassetbreakdown',
            name='updateIndex',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='holding',
            name='isNAVValued',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='holdingassetbreakdown',
            name='holding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assetBreakdowns', to='data.Holding'),
        ),
        migrations.AlterField(
            model_name='userhistoricalholding',
            name='portfolioIndex',
            field=models.PositiveIntegerField(),
        ),
    ]