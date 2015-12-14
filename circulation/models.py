from django.db import models
from django.contrib.contenttypes import fields as ct_fields
from django.contrib.contenttypes import models as ct_models


class Issue(models.Model):
    resource = models.ForeignKey('catalog.ResourceInstance')
    patron = models.ForeignKey('patron.Patron')
    loan_at = models.DateTimeField()


    def __str__(self):
        data = {
            'resource': self.resource_object,
            'loan_date': self.loan_at.date(),
            'borrower': self.patron
        }
        return "{resource} [borrow: {loan_date} by {borrower}]".format(**data)


class Return(models.Model):
    issue = models.OneToOneField('circulation.Issue')

    return_at = models.DateTimeField()

    def __str__(self):
        return "{} [return: {}]".format(self.lend, self.return_at.date())
