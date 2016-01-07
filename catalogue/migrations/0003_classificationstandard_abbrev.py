# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_auto_20160106_0412'),
    ]

    operations = [
        migrations.AddField(
            model_name='classificationstandard',
            name='abbrev',
            field=models.CharField(max_length=10, default=1),
            preserve_default=False,
        ),
    ]
