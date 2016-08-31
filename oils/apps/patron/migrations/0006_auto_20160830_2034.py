# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-30 20:34
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('patron', '0005_auto_20160830_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='patron',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patron',
            name='country',
            field=django_countries.fields.CountryField(default='SG', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patron',
            name='note',
            field=models.TextField(blank=True, help_text='Extra Information for Administrator'),
        ),
        migrations.AddField(
            model_name='patron',
            name='notification_type',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AddField(
            model_name='patron',
            name='postcode',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]
