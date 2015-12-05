from django.db import models


class Book(models.Model):
    info = models.ForeignKey('BookInfo')

    def __str__(self):
        return self.info.isbn13


class BookInfo(models.Model):
    isbn13 = models.CharField(max_length=13)
    isbn10 = models.CharField(max_length=10)
    title = models.CharField(max_length=255) 
    subtitle = models.TextField()
    abstract = models.TextField()
    authors = models.ManyToManyField('authorities.Author')

    def __str__(self):
        return self.isbn13
