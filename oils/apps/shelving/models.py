from django.db import models

from django.contrib.contenttypes import models as ct_models
from django.contrib.contenttypes import fields as ct_fields

from django_extensions.db import fields as ext_fields

class Item(models.Model):
    """
    Item Record. (ie. Library Book Copy)
    """
    code = models.CharField(max_length=50)

    RESOURCE_CHOICES = (models.Q(app_label='catalog', model='book'))

    creative_work_type = models.ForeignKey(ct_models.ContentType,
            limit_choices_to=RESOURCE_CHOICES)
    creative_work_id = models.UUIDField()
    creative_work_object = ct_fields.GenericForeignKey(
            'creative_work_type', 'creative_work_id')

    location = models.ForeignKey('Location', blank=True, null=True)

    def __str__(self):
        return "[{}] {}".format(self.code, self.creative_work_object)

    @property
    def resource_identifiers(self):
        return self.creative_work_object.resource_identifiers

    @property
    def book(self):
        return self.creative_work_object

class Location(models.Model):
    """
    Physical Location of the library. 
    Possible value such as Reference, General, Children, etc.
    """
    name = models.CharField(max_length=100)
    slug = ext_fields.AutoSlugField(max_length=100, unique=True,
            populate_from='name')

    def __str__(self):
        return self.name
