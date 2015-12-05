from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    aliases = models.ForeignKey('authorities.AuthorAlias')

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

class AuthorAlias(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
