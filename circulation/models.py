from django.db import models
from django.contrib.contenttypes import fields as ct_fields
from django.contrib.contenttypes import models as ct_models


class Issue(models.Model):
    patron = models.ForeignKey('patron.Patron')
    loan_at = models.DateTimeField()

    lend_item = models.Q(app_label='catalog', model='book')
    resource_type = models.ForeignKey(ct_models.ContentType,
            limit_choices_to=lend_item)
    resource_id = models.PositiveIntegerField()
    resource_object = ct_fields.GenericForeignKey(
            'resource_type', 'resource_id')

    def __str__(self):
        data = {
            'resource': self.resource_object,
            'loan_date': self.loan_at.date(),
            'borrower': self.patron
        }
        return "{resource} [borrow: {loan_date} by {borrower}]".format(**data)


class Return(models.Model):
    lend = models.OneToOneField('circulation.Lend')

    return_at = models.DateTimeField()

    def __str__(self):
        return "{} [return: {}]".format(self.lend, self.return_at.date())
