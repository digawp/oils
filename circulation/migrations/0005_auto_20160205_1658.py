# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circulation', '0004_auto_20151228_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuerenewal',
            name='renew_at',
            field=models.DateTimeField(),
        ),
    ]
