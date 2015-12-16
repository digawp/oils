# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
        ('patron', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('loan_at', models.DateTimeField()),
                ('patron', models.ForeignKey(to='patron.Patron')),
                ('resource', models.ForeignKey(to='catalogue.ResourceInstance')),
            ],
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('return_at', models.DateTimeField()),
                ('issue', models.OneToOneField(to='circulation.Issue')),
            ],
        ),
    ]
