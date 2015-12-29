# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circulation', '0002_issuerenewal'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueReturn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('return_at', models.DateTimeField()),
                ('issue', models.OneToOneField(to='circulation.Issue')),
            ],
        ),
        migrations.RemoveField(
            model_name='return',
            name='issue',
        ),
        migrations.DeleteModel(
            name='Return',
        ),
    ]
