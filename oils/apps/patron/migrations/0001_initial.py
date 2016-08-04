# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-04 08:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patron',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identification', models.CharField(max_length=30, unique=True)),
                ('loan_duration', models.IntegerField(default=15)),
                ('loan_limit', models.IntegerField(default=2)),
                ('renewal_limit', models.IntegerField(default=3)),
            ],
        ),
    ]
