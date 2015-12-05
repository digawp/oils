from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    aliases = models.ForeignKey('authorities.AuthorAlias')

class AuthorAlias(models.Model):
    name = models.CharField(max_length=255)
