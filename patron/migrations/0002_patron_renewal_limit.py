# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patron', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patron',
            name='renewal_limit',
            field=models.IntegerField(default=3),
        ),
    ]
