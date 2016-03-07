# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patron', '0003_patron_loan_duration'),
        ('catalogue', '0003_classificationstandard_abbrev'),
        ('circulation', '0005_auto_20160205_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('loan_at', models.DateTimeField(auto_now_add=True)),
                ('patron', models.ForeignKey(to='patron.Patron')),
                ('resource', models.ForeignKey(to='catalogue.ResourceInstance')),
            ],
        ),
        migrations.CreateModel(
            name='LoanRenewal',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('renew_at', models.DateTimeField()),
                ('loan', models.ForeignKey(to='circulation.Loan')),
            ],
        ),
        migrations.CreateModel(
            name='LoanReturn',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('return_at', models.DateTimeField(auto_now_add=True)),
                ('loan', models.OneToOneField(to='circulation.Loan')),
            ],
        ),
        migrations.RemoveField(
            model_name='issue',
            name='patron',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='resource',
        ),
        migrations.RemoveField(
            model_name='issuerenewal',
            name='issue',
        ),
        migrations.RemoveField(
            model_name='issuereturn',
            name='issue',
        ),
        migrations.DeleteModel(
            name='Issue',
        ),
        migrations.DeleteModel(
            name='IssueRenewal',
        ),
        migrations.DeleteModel(
            name='IssueReturn',
        ),
    ]
