# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circulation', '0003_auto_20151224_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='loan_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='issuerenewal',
            name='renew_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='issuereturn',
            name='return_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
