# -*- coding: utf-8 -*-
# Generated by Django 1.11a1 on 2017-04-21 20:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0050_userfee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Benchmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=225)),
                ('age_group', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Benchmark',
                'verbose_name_plural': 'Benchmarks',
            },
        ),
        migrations.CreateModel(
            name='BenchmarkComposite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('benchmark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.Benchmark')),
                ('holding_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, to='data.Holding'))
            ],
            options={
                'verbose_name': 'BenchmarkComposite',
                'verbose_name_plural': 'BenchmarkComposites',
            },
        ),
    ]
