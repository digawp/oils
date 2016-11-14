import factory
from . import models

class BookFactory(factory.django.DjangoModelFactory):
    """Raw Book Factory (empty data)"""

    class Meta:
        model = models.Book

class IdentifierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UniversalIdentifier
    id_type = factory.Iterator(models.UniversalIdentifierType.objects.all())
    value = factory.Sequence(lambda i: '{:0=10d}'.format(i))

class ISBNFactory(IdentifierFactory):
    id_type = models.UniversalIdentifierType.objects.get(name='isbn')

class LCCNFactory(IdentifierFactory):
    id_type = models.UniversalIdentifierType.objects.get(name='lccn')
    
class BookIdentifierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BookIdentifier
    book = factory.SubFactory(BookFactory)
    identifier = factory.SubFactory(IdentifierFactory)

class LibraryBookFactory(BookFactory):
    """Book Factory used for testing (filled with mock data)"""

    isbn = factory.RelatedFactory(
        BookIdentifierFactory, 'book',
        identifier=ISBNFactory())
    lccn = factory.RelatedFactory(
        BookIdentifierFactory, 'book',
        identifier=LCCNFactory())
