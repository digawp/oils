# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('call_number', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ClassificationStandard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('slug', django_extensions.db.fields.AutoSlugField(max_length=100, editable=False, blank=True, populate_from='name', unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='classification',
            name='standard',
            field=models.ForeignKey(to='catalogue.ClassificationStandard'),
        ),
        migrations.AddField(
            model_name='book',
            name='classification',
            field=models.ForeignKey(to='catalogue.Classification', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resourceinstance',
            name='location',
            field=models.ForeignKey(to='catalogue.Location', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='serial',
            name='classification',
            field=models.ForeignKey(to='catalogue.Classification', default=1),
            preserve_default=False,
        ),
    ]
