# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-28 06:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_module_moduleid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='isAddOn',
        ),
    ]
