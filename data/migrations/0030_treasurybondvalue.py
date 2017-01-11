# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-10 21:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0029_holdingdividends'),
    ]

    operations = [
        migrations.CreateModel(
            name='TreasuryBondValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('value', models.FloatField()),
            ],
        ),
    ]
