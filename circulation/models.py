from django.db import models
from django.contrib.contenttypes import fields as ct_fields
from django.contrib.contenttypes import models as ct_models


class Lend(models.Model):
    patron = models.ForeignKey('patron.Patron')
    loan_at = models.DateTimeField()

    lend_item = models.Q(app_label='catalog', model='book')
    content_type = models.ForeignKey(ct_models.ContentType,
            limit_choices_to=lend_item)
    object_id = models.PositiveIntegerField()
    content_object = ct_fields.GenericForeignKey('content_type', 'object_id')


class Return(models.Model):
    book = models.ForeignKey('catalog.Book')
    lend = models.OneToOneField('circulation.Lend')
