from django.db import models

from django_extensions.db import fields as ext_fields


class AbstractResourceInfo(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=False)
    abstract = models.TextField(blank=True)

    subjects = models.ManyToManyField('subject.Subject')
    authorities = models.ManyToManyField('authorities.Authority')

    width = models.FloatField()
    height = models.FloatField()

    class Meta:
        abstract = True


class AbstractResource(models.Model):
    code = models.CharField(max_length=128)

    class Meta:
        abstract = True


class Book(AbstractResource):
    info = models.ForeignKey('BookInfo')

    def __str__(self):
        return self.info.isbn13


class BookInfo(AbstractResource):
    isbn13 = models.CharField(max_length=13)
    isbn10 = models.CharField(max_length=10)
    subtitle = models.TextField()

    def __str__(self):
        return self.isbn13

