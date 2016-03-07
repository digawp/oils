# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_classificationstandard_abbrev'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classification',
            name='standard',
        ),
        migrations.AlterField(
            model_name='book',
            name='classification',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='serial',
            name='classification',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.DeleteModel(
            name='Classification',
        ),
        migrations.DeleteModel(
            name='ClassificationStandard',
        ),
    ]
