from django.db import models
from django.contrib.contenttypes import fields as ct_fields
from django.contrib.contenttypes import models as ct_models

from django.utils.translation import ugettext_lazy as _

from django_extensions.db import fields as ext_fields


class AbstractResource(models.Model):
    """
    This abstract model holds the bibliographic record of all resources
    """
    title = models.CharField(max_length=250)
    subtitle = models.TextField()

    slug = models.SlugField(max_length=250, unique=False)

    abstract = models.TextField(blank=True)

    subjects = models.ManyToManyField('subject.Subject')
    authors = models.ManyToManyField('Author')
    publisher = models.ForeignKey('Publisher')

    class Meta:
        abstract = True


class Author(models.Model):
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
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Resource(models.Model):
    """
    The physical resource.
    For example Book Abc could have multiple copies of it.
    """
    code = models.CharField(max_length=50)

    RESOURCE_CHOICES = (
        models.Q(app_label='catalog', model='serial')|
        models.Q(app_label='catalog', model='book'))

    resource_type = models.ForeignKey(ct_models.ContentType,
            limit_choices_to=RESOURCE_CHOICES)
    resource_id = models.PositiveIntegerField()
    resource_object = ct_fields.GenericForeignKey(
            'resource_type', 'resource_id')

    def __str__(self):
        return self.resource_object


class Book(AbstractResource):
    isbn13 = models.CharField(max_length=13)
    isbn10 = models.CharField(max_length=10)

    def __str__(self):
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


class Serial(AbstractResource):
    """
    The Information about a particular serial.
    (e.g. Django Magazine, Newspaper Techno, etc...)
    """
    issn = models.CharField(max_length=8)

    # Serial can be in many types or forms, we call this serial class
    serial_type = models.ForeignKey('SerialType')

    def __str__(self):
        return self.issn



"""
class Attribute(models.Model):
    serial_class = models.ForeignKey('SerialClass', blank=True, null=True)

    name = models.CharField(max_length=100)

    TEXT = 'text'
    INTEGER = 'integer'
    BOOLEAN = 'boolean'
    FLOAT = 'float'
    DATE = 'date'
    TYPE_CHOICES = (
        (TEXT, _('Text')),
        (INTEGER, _('Integer')),
        (BOOLEAN, _('True / False')),
        (FLOAT, _('Float')),
        (DATE, _('Date')),
    )

    datatype = models.CharField(max_length=20,
            choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0])   
    required = models.BooleanField(default=False)


class AttributeValue(models.Model):
    attribute = models.ForeignKey('Attribute')
    serial = models.ForeignKey('Serial')
    

    value_text = models.TextField(blank=True, null=True)
    value_integer = models.IntegerField(blank=True, null=True)
    value_boolean = models.NullBooleanField(blank=True)
    value_float = models.FloatField(blank=True, null=True)
    value_date = models.DateField(blank=True, null=True)
"""
