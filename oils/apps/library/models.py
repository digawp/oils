from django.db import models
from django.db.models import signals


# Create your models here.
class BookAnnotation(models.Model):
    book = models.OneToOneField('catalog.Book')

    abstract = models.TextField(help_text='Book Abstract', blank=True)
    note = models.TextField(blank=True)

    volume = models.CharField(max_length=50, blank=True)
    edition = models.CharField(max_length=50, blank=True)
    issue = models.CharField(max_length=50, blank=True)
    revision = models.CharField(max_length=50, blank=True)
    series = models.CharField(max_length=150, blank=True)


    pages = models.IntegerField(blank=True, null=True)
    height = models.FloatField(help_text='Book Height (cm)',
            blank=True, null=True)
    price = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=9)

def create_bookannotation(sender, instance, created, **kwargs):
    if created:
        BookAnnotation.objects.create(book=instance)

signals.post_save.connect(create_bookannotation, sender='catalog.Book',
        weak=False, dispatch_uid='models.create_bookannotation')
