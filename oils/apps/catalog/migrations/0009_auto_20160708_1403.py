# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-08 14:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20160708_1402'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agent',
            old_name='full_name',
            new_name='name',
        ),
    ]
