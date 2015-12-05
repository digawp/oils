from django.db import models


class Patron(models.Model):
    user = models.OneToOneField('auth.User')
    loan_limit = models.IntegerField(default=2)
