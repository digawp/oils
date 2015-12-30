from django.db import models

from registration import signals


class Patron(models.Model):
    user = models.OneToOneField('auth.User')
    loan_limit = models.IntegerField(default=2)

    def __str__(self):
        return self.user.username

def create_patron(sender, **kwargs):
    patron = Patron(user=kwargs.get('user'))
    patron.save()

signals.user_registered.connect(create_patron)
