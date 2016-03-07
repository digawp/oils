from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes import fields as ct_fields
from django.contrib.contenttypes import models as ct_models


from . import get_backend


class LoanRenewalManager(models.Manager):
    def get_last_renewal(self, loan):
        return self.filter(loan=loan).order_by('renew_at').last()


class Loan(models.Model):
    resource = models.ForeignKey('catalogue.ResourceInstance')
    patron = models.ForeignKey('patron.Patron')
    loan_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        data = {
            'resource': self.resource.resource_identifier,
            'loan_date': self.loan_at.date(),
            'borrower': self.patron
        }
        return "[{resource}] [borrow: {loan_date} by {borrower}]".format(**data)

    def renew(self):
        backend = get_backend()
        backend.renew(loan=self)


class LoanRenewal(models.Model):
    loan = models.ForeignKey('Loan')

    renew_at = models.DateTimeField()

    objects = LoanRenewalManager()

    def __str__(self):
        return "{} [extend: {}]".format(self.loan, self.renew_at.date())

    def clean(self):
        backend = get_backend()
        backend.validate(self.loan)


class LoanReturn(models.Model):
    loan = models.OneToOneField('circulation.Loan')

    return_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} [return: {}]".format(self.loan, self.return_at.date())
