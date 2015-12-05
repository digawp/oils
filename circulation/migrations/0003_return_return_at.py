# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('circulation', '0002_auto_20151205_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='return',
            name='return_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 5, 19, 21, 7, 871653, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
