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

from django.db import models
from django.db.models import Q, F
from django.db.models.aggregates import Count
from django.contrib.contenttypes import fields as ct_fields
from django.contrib.contenttypes import models as ct_models
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

from django_extensions.db import fields as ext_fields


class AbstractResourceCreativeWork(models.Model):
    """
    CreativeWork models
    """
    title = models.CharField(max_length=250)
    subtitle = models.TextField()

    slug = models.SlugField(max_length=250, unique=False)

    abstract = models.TextField(blank=True)

    subjects = models.ManyToManyField('subject.Subject')
    authors = models.ManyToManyField('Author')
    publisher = models.ForeignKey('Publisher')

    classification = models.CharField(max_length=20, blank=True)

    class Meta:
        abstract = True


    @property
    def resource_type(self):
        return self._meta.model_name


    
    def get_absolute_url(self):
        return reverse('catalogue:detail', kwargs={
            'resourcetype': self.resource_type,
            'slug': self.slug,
        })



class Book(AbstractResourceCreativeWork):
    """
    CreativeWork models
    """
    isbn13 = models.CharField(max_length=13)
    isbn10 = models.CharField(max_length=10)

    instances = ct_fields.GenericRelation('ResourceInstance',
            content_type_field='creative_work_type',
            object_id_field='creative_work_id',
            related_query_name='books')

    def __str__(self):
        return self.isbn13

    @property
    def resource_identifier(self):
        return self.isbn13


class SerialType(models.Model):
    """
    Different type of Serial
    (e.g. Magazine, Newspaper, Journal, etc..)
    """
    name = models.CharField(max_length=100)
    slug = ext_fields.AutoSlugField(max_length=100, unique=True,
            populate_from='name')

    def __str__(self):
        return self.name


class Serial(AbstractResourceCreativeWork):
    """
    Bibliographic record.
    """
    issn = models.CharField(max_length=8)

    instances = ct_fields.GenericRelation('ResourceInstance',
            content_type_field='creative_work_type',
            object_id_field='creative_work_id',
            related_query_name='serials')

    # Serial can be in many types or forms, we call this serial class
    serial_type = models.ForeignKey('SerialType')

    def __str__(self):
        return self.issn

    @property
    def resource_type(self):
        return self.serial_type.slug

    @property
    def resource_identifier(self):
        return self.issn


class ResourceInstanceQuerySet(models.QuerySet):
    def available(self):
        return self.annotate(
                loan_count=Count('loan'),
                return_count=Count('loan__loanreturn')
            ).filter(Q(loan_count=F('return_count')))

    def unavailable(self):
        return self.annotate(
                loan_count=Count('loan'),
                return_count=Count('loan__loanreturn')
            ).exclude(Q(loan_count=F('return_count')))

class ResourceInstance(models.Model):
    """
    Holding Record or Item Record.
    """
    code = models.CharField(max_length=50)

    RESOURCE_CHOICES = (
        models.Q(app_label='catalogue', model='serial')|
        models.Q(app_label='catalogue', model='book'))

    creative_work_type = models.ForeignKey(ct_models.ContentType,
            limit_choices_to=RESOURCE_CHOICES)
    creative_work_id = models.PositiveIntegerField()
    creative_work_object = ct_fields.GenericForeignKey(
            'creative_work_type', 'creative_work_id')

    objects = ResourceInstanceQuerySet.as_manager()

    location = models.ForeignKey('Location')

    @property
    def resource_type(self):
        return self.creative_work_object.resource_type

    @property
    def resource_identifier(self):
        if self.creative_work_type.model == 'serial':
            return self.creative_work_object.issn
        else:
            return self.creative_work_object.isbn13


    def __str__(self):
        return "[{}] {}".format(self.code, self.creative_work_object)


class Location(models.Model):
    name = models.CharField(max_length=100)
    slug = ext_fields.AutoSlugField(max_length=100, unique=True,
            populate_from='name')

    def __str__(self):
        return self.name


class Author(models.Model):
    """
    Authority Record for Author
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name).strip()


class AuthorAlias(models.Model):
    """
    Author aliases: 
    For example `John Doe` may have multiple aliases:
    - Doe, J.
    - Doe J
    - Doe
    - The Doe
    """
    name = models.CharField(max_length=100)
    author = models.ForeignKey('Author')

    def __str__(self):
        return self.name


class Publisher(models.Model):
    """
    Authority Record for Publisher
    """
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
