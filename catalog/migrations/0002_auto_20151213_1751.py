# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serial',
            name='serial_type',
            field=models.ForeignKey(to='catalog.SerialType', default=1),
            preserve_default=False,
        ),
    ]
