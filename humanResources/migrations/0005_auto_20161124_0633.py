# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-24 06:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('humanResources', '0004_auto_20161009_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setupuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='setupuser',
            name='last_name',
        ),
    ]