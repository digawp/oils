# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-30 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patron', '0004_auto_20160830_0906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='register_at',
        ),
        migrations.AddField(
            model_name='membership',
            name='register_on',
            field=models.DateField(blank=True, null=True),
        ),
    ]
