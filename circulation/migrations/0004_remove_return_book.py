# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circulation', '0003_return_return_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='return',
            name='book',
        ),
    ]
