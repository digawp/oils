# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-08 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20160708_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='birth',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='agent',
            name='death',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
