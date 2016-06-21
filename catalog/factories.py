import factory
from . import models

class BookFactory(factory.django.DjangoModelFactory):
    """Raw Book Factory (empty data)"""

    class Meta:
        model = models.Book

    
class BookIdentifierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BookIdentifier
    book = factory.SubFactory(BookFactory)
    id_type = factory.Iterator(models.BookIdentifierType.objects.all())
    value = factory.Sequence(lambda i: '{:0=10d}'.format(i))

class LibraryBookFactory(BookFactory):
    """Book Factory used for testing (filled with mock data)"""

    isbn = factory.RelatedFactory(
        BookIdentifierFactory, 'book', id_type=models.BookIdentifierType.objects.get(name='isbn'))
    lccn = factory.RelatedFactory(
        BookIdentifierFactory, 'book', id_type=models.BookIdentifierType.objects.get(name='lccn'))
