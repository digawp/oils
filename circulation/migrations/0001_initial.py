# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patron', '0001_initial'),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('loan_at', models.DateTimeField()),
                ('patron', models.ForeignKey(to='patron.Patron')),
                ('resource', models.ForeignKey(to='catalog.ResourceInstance')),
            ],
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('return_at', models.DateTimeField()),
                ('issue', models.OneToOneField(to='circulation.Issue')),
            ],
        ),
    ]
