# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-23 20:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_quovouser_didlink'),
        ('data', '0019_auto_20161222_0121'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSharpe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('value', models.FloatField()),
                ('quovoUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userSharpes', to='dashboard.QuovoUser')),
            ],
            options={
                'verbose_name': 'UserSharpe',
                'verbose_name_plural': 'UserSharpes',
            },
        ),
    ]