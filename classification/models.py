from django.db import models


class ResourceClassification(models.Model):
    name = models.CharField(max_length=128)
    resource = models.OneToOneField('catalog.Resource')
