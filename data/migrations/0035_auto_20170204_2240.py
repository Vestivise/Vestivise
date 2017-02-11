# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-04 22:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0034_auto_20170129_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='holding',
            name='sector',
            field=models.CharField(blank=True, default=b'', max_length=22, null=True),
        ),
        migrations.AlterField(
            model_name='holding',
            name='category',
            field=models.CharField(choices=[(b'MUTF', b'Mutual Fund'), (b'CASH', b'Cash'), (b'STOC', b'Stock'), (b'FOFF', b'Fund of Funds'), (b'IGNO', b'Should Ignore'), (b'BOND', b'Bond')], default=b'IGNO', max_length=4),
        ),
    ]