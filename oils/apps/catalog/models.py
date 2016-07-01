"""
Bibframe model consists of the following main classes:

- CreativeWork:
    a resource reflecting a conceptual essence of the cataloging item 

- Instance:
    a resource reflecting an individual, 
    material embodiment of the work.

- Authority:
    a resource reflecting key authority concept that have defined
    relationship reflected in the Work and Instance.
    Examples of Authority Resources include 
    People, Places, Topics, Organizations, etc.

- Annotation:
    a resouce that decorates other BIBFRAME resources with additional
    information. examples of such annotations include Library
    Holdings information, cover art and reviews.
"""
import uuid
import json
from functools import reduce
from django.db import models
from django.db.models import Q, F
from django.db.models.aggregates import Count
from django.contrib.contenttypes import fields as ct_fields
from django.contrib.contenttypes import models as ct_models
from django.contrib.postgres import fields as pg_fields
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

from mptt import models as mptt_models
from . import openlibrary

from .bibkey import Bibkey

class BookIdentifierTypeQuerySet(models.QuerySet):
    def bibkey_list(self):
        result = self.all().values_list('name', flat=True)
        return result


class BookIdentifierType(models.Model):
    name = models.CharField(max_length=25, unique=True)

    objects = BookIdentifierTypeQuerySet.as_manager()

    def __str__(self):
        return self.name


class BookIdentifierQuerySet(models.QuerySet):
    def identifiers_list(self):
        return {
            bib['id_type__name']: bib['value']
            for bib in self.values('id_type__name', 'value')}


class BookIdentifier(models.Model):
    id_type = models.ForeignKey('BookIdentifierType')
    book = models.ForeignKey('Book', related_name='identifiers')
    value = models.CharField(max_length=16)

    objects = BookIdentifierQuerySet.as_manager()

    class Meta:
        unique_together = ('id_type', 'value')

    def __str__(self):
        return '{}:{}'.format(self.id_type.name, self.value)


class ClassificationType(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class Classification(models.Model):
    classification_type = models.ForeignKey('ClassificationType')
    value = models.CharField(max_length=25)

    class Meta:
        unique_together = ('classification_type', 'value')

    def __str__(self):
        return '{}:{}'.format(self.classification_type.name, self.value)

    @staticmethod
    def autocomplete_search_fields():
        """grappelli (django admin) autocomplete search"""
        return ("value__icontains",)


class Subject(mptt_models.MPTTModel):
    name = models.CharField(max_length=128)
    parent = mptt_models.TreeForeignKey('self', null=True, blank=True,
            related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        if not self.parent:
            return self.name
        else:
            return str(self.parent) + " > " + self.name


class BookQuerySet(models.QuerySet):
    def retrieve(self, bibkey):
        """Retrieve/get a single book object"""
        if isinstance(bibkey, str):
            bibkey = Bibkey.parse(bibkey)

        assert isinstance(bibkey, Bibkey)
        return self.get(identifiers__id_type__name=bibkey.bibtype,
                identifiers__value=bibkey.bibvalue)

    def lookup(self, bibkeys):
        """Lookup/filter for books queryset"""
        if isinstance(bibkeys, str):
            bibkeys = Bibkey.parse(bibkeys)

        assert isinstance(bibkeys, list)
        assert all(isinstance(bibkey, Bibkey) for bibkey in bibkeys)

        query = reduce(
            lambda q, bibkey: (q | Q(
                identifiers__id_type__name=bibkey.bibtype,
                identifiers__value=bibkey.bibvalue)),
            bibkeys, Q())

        return self.filter(query)


class Agent(models.Model):
    identifiers = models.ManyToManyField('AgentIdentifier', blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name).strip()

    @staticmethod
    def autocomplete_search_fields():
        """grappelli (django admin) autocomplete search"""
        return ("first_name__icontains", "last_name__icontains",)


class Role(models.Model):
    """Author, Contributor, Editor, Illustrator, etc..."""
    label = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return self.label


class BookAgent(models.Model):
    agent = models.ForeignKey('Agent')
    book = models.ForeignKey('Book')
    role = models.ForeignKey('Role')

    def __str__(self):
        return "{book} by {agent} ({role})".format(**{
            'book': self.book,
            'agent': self.agent,
            'role': self.agent
        })

class Series(models.Model):
    title = models.CharField(max_length=250)
    books = models.ManyToManyField('Book', through='BookSeries')


class BookSeries(models.Model):
    book = models.ForeignKey('Book')
    series = models.ForeignKey('Series')

    volume = models.IntegerField()
    edition = models.IntegerField()


class Book(models.Model):
    """
    CreativeWork models
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=250)
    subtitle = models.TextField(blank=True)

    subjects = models.ManyToManyField('Subject', blank=True)
    classifications = models.ManyToManyField('Classification', blank=True)
    agents = models.ManyToManyField('Agent', through='BookAgent', blank=True)
    publishers = models.ManyToManyField('Publisher', through='Publication', blank=True)

    objects = BookQuerySet.as_manager()

    def __str__(self):
        return self.title

    def to_generic_bibliographic(self):
        return GenericBibliographic(**self.__dict__)

    @property
    def resource_type(self):
        return 'book'

    @property
    def resource_identifiers(self):
        return self.identifiers.identifiers_list()


class AgentIdentifierType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class AgentIdentifier(models.Model):
    id_type = models.ForeignKey('AgentIdentifierType')
    value = models.CharField(max_length=40)

    class Meta:
        unique_together = ('id_type', 'value')

    def __str__(self):
        return '{}:{}'.format(self.id_type, self.value)


class AgentAlias(models.Model):
    """
    Agent aliases: 
    For example `John Doe` may have multiple aliases:
    - Doe, J.
    - Doe J
    - Doe
    - The Doe
    """
    name = models.CharField(max_length=100)
    agent = models.ForeignKey('Agent')

    def __str__(self):
        return self.name


class Publisher(models.Model):
    """
    Authority Record for Publisher
    """
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        """grappelli (django admin) autocomplete search"""
        return ("name__icontains",)


class Publication(models.Model):
    publisher = models.ForeignKey('Publisher')
    book = models.ForeignKey('Book')
    year = models.SmallIntegerField()

    def __str__(self):
        return '{} ({}) @ {}'.format(self.book, self.year, self.publisher.name)


class OpenLibraryQuerySet(models.QuerySet):
    def retrieve(self, bibkey):
        """Retrieve/Get an OpenLibrary object"""
        if isinstance(bibkey, str):
            bibkey = Bibkey.parse(bibkey)

        try:
            obj = self.get(id_type__name=bibkey.bibtype,
                    id_value=bibkey.bibvalue)
        except self.model.DoesNotExist:
            result = openlibrary.search((bibkey.bibtype, bibkey.bibvalue))
            id_type=BookIdentifierType.objects.get(name=bibkey.bibtype)
            obj = self.model.objects.create(
                    id_type=id_type,
                    id_value=bibkey.bibvalue,
                    raw_json=result)
        return obj

    def lookup(self, bibkeys):
        """Lookup for OpenLibrary QuerySet"""
        if isinstance(bibkeys, str):
            bibkeys = Bibkey.parse(bibkeys)

        assert isinstance(bibkeys, list)
        assert all(isinstance(bibkey, Bibkey) for bibkey in bibkeys)

        objs = [self.retrieve(bibkey) for bibkey in bibkeys]
        return self.filter(pk__in=objs)

class GenericBibliographic(object):
    def __init__(self, *args, **kwargs):
        self.title = kwargs.get('title', '')
        self.identifiers = kwargs.get('identifiers', {})
        self.agents = kwargs.get('agents', {})
        self.publishers = kwargs.get('publishers', {})
        self.classification = kwargs.get('classification', {})
        self.subjects = kwargs.get('subjects', {})


class OpenLibrary(models.Model):
    id_type = models.ForeignKey('BookIdentifierType')
    id_value = models.CharField(max_length=16)
    raw_json = pg_fields.JSONField()
    oils_book = models.OneToOneField('Book', null=True, blank=True)

    objects = OpenLibraryQuerySet.as_manager()

    def __str__(self):
        return "{}:{}".format(self.id_type, self.id_value)

    def to_generic_bibliographic(self):
        if not self.raw_json:
            return None

        bib_kwargs = self.raw_json
        if 'identifiers' in bib_kwargs:
            identifiers = bib_kwargs['identifiers']
            if 'isbn_13' in identifiers or 'isbn_10' in identifiers:
                bib_kwargs['identifiers']['isbn'] = []

                # ISBN13
                isbn13 = identifiers.get('isbn_13')
                if isbn13:
                    for _ in isbn13:
                        bib_kwargs['identifiers']['isbn'].append(_)
                    del bib_kwargs['identifiers']['isbn_13']

                # ISBN10
                isbn10 = identifiers.get('isbn_10')
                if isbn10:
                    for _ in isbn10:
                        bib_kwargs['identifiers']['isbn'].append(_)
                    del bib_kwargs['identifiers']['isbn_10']

        return GenericBibliographic(**bib_kwargs)
