# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-14 22:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('humanResources', '0009_remove_humanresourceprofile_employee_estimate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='humanresourceprofile',
            name='subscription_date',
            field=models.DateField(default=datetime.datetime(2017, 1, 14, 22, 58, 54, 830857, tzinfo=utc)),
        ),
    ]