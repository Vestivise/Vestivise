# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-03 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0010_investmentoption_threeyearreturn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yodleeaccount',
            name='accountNumber',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
