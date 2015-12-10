from django.db import models


class Authority(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    aliases = models.ForeignKey('authorities.AuthorityAlias')

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

class AuthorityAlias(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
