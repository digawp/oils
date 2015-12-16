# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('bio', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='AuthorAlias',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('author', models.ForeignKey(to='catalogue.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=250)),
                ('subtitle', models.TextField()),
                ('slug', models.SlugField(max_length=250)),
                ('abstract', models.TextField(blank=True)),
                ('isbn13', models.CharField(max_length=13)),
                ('isbn10', models.CharField(max_length=10)),
                ('authors', models.ManyToManyField(to='catalogue.Author')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='ResourceInstance',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('code', models.CharField(max_length=50)),
                ('creative_work_id', models.PositiveIntegerField()),
                ('creative_work_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Serial',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=250)),
                ('subtitle', models.TextField()),
                ('slug', models.SlugField(max_length=250)),
                ('abstract', models.TextField(blank=True)),
                ('issn', models.CharField(max_length=8)),
                ('authors', models.ManyToManyField(to='catalogue.Author')),
                ('publisher', models.ForeignKey(to='catalogue.Publisher')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SerialType',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('slug', django_extensions.db.fields.AutoSlugField(unique=True, editable=False, populate_from='name', blank=True, max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='serial',
            name='serial_type',
            field=models.ForeignKey(to='catalogue.SerialType'),
        ),
        migrations.AddField(
            model_name='serial',
            name='subjects',
            field=models.ManyToManyField(to='subject.Subject'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(to='catalogue.Publisher'),
        ),
        migrations.AddField(
            model_name='book',
            name='subjects',
            field=models.ManyToManyField(to='subject.Subject'),
        ),
    ]
