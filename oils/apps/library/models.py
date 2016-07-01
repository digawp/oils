from django.db import models


# Create your models here.
class BookAnnotation(models.Model):
    book = models.OneToOneField('catalog.Book')
    abstract = models.TextField(help_text='Book Abstract', blank=True)
    pages = models.IntegerField(blank=True)
    note = models.TextField(blank=True)
    height = models.IntegerField(help_text='Book Height (cm)', blank=True)

