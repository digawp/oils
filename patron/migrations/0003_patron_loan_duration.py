# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patron', '0002_patron_renewal_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='patron',
            name='loan_duration',
            field=models.IntegerField(default=15),
        ),
    ]
