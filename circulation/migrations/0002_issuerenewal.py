# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circulation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueRenewal',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('renew_at', models.DateTimeField()),
                ('issue', models.ForeignKey(to='circulation.Issue')),
            ],
        ),
    ]
