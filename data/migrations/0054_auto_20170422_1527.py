# -*- coding: utf-8 -*-
# Generated by Django 1.11a1 on 2017-04-22 15:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0053_data_migration_benchmark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='benchmark',
            name='one_month_returns',
        ),
        migrations.RemoveField(
            model_name='benchmark',
            name='one_year_returns',
        ),
        migrations.RemoveField(
            model_name='benchmark',
            name='three_month_returns',
        ),
        migrations.RemoveField(
            model_name='benchmark',
            name='three_year_returns',
        ),
        migrations.RemoveField(
            model_name='benchmark',
            name='two_year_returns',
        ),
        migrations.RemoveField(
            model_name='benchmark',
            name='year_to_date_returns',
        ),
        migrations.RemoveField(
            model_name='benchmarkcomposite',
            name='id',
        ),
        migrations.AlterField(
            model_name='benchmarkcomposite',
            name='benchmark',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='composites', to='data.Benchmark'),
        ),
    ]
