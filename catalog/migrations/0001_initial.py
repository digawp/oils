# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('isbn13', models.CharField(max_length=13)),
                ('isbn10', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.TextField()),
                ('abstract', models.TextField()),
                ('authors', models.ManyToManyField(to='authorities.Author')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='info',
            field=models.ForeignKey(to='catalog.BookInfo'),
        ),
    ]
