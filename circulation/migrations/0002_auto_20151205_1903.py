# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circulation', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lend',
            old_name='object_id',
            new_name='resource_id',
        ),
        migrations.RenameField(
            model_name='lend',
            old_name='content_type',
            new_name='resource_type',
        ),
    ]
