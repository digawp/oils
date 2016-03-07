from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.contenttypes import fields as ct_fields
from django.contrib.contenttypes import models as ct_models


from . import get_backend


class LoanRenewalManager(models.Manager):
    def get_last_renewal(self, loan):
        return self.filter(loan=loan).order_by('renew_at').last()

class LoanManager(models.Manager):
    def create_loan(self, patron, *args, **kwargs):
        if not self.last().is_returned:
            raise ValueError("Resource has not been returned")
        return self.create(resource=self.instance, 
            patron=patron, *args, **kwargs)


class Loan(models.Model):
    resource = models.ForeignKey('catalogue.ResourceInstance')
    patron = models.ForeignKey('patron.Patron')
    loan_at = models.DateTimeField(auto_now_add=True)

    objects = LoanManager()

    def __str__(self):
        data = {
            'resource': self.resource.resource_identifier,
            'loan_date': self.loan_at.date(),
            'borrower': self.patron
        }
        return "[{resource}] [borrow: {loan_date} by {borrower}]".format(**data)

    @property
    def is_returned(self):
        if self.pk: #  Existing Loan (check the loan return record)
            try:
                return self.loanreturn is not None
            except ObjectDoesNotExist:
                return False
        else: # New Loan (check the resource)
            return self.resource.is_available


    def renew(self):
        backend = get_backend()
        backend.renew(loan=self)

    def clean(self):
        if not self.pk and self.resource_id and not self.is_returned:
            raise ValidationError({
                'resource': 'Resource is not available'
            })




class LoanRenewal(models.Model):
    loan = models.ForeignKey('Loan')

    renew_at = models.DateTimeField()

    objects = LoanRenewalManager()

    def __str__(self):
        return "{} [extend: {}]".format(self.loan, self.renew_at.date())

    def clean(self):
        if self.loan_id:
            backend = get_backend()
            backend.validate(self.loan)


class LoanReturn(models.Model):
    loan = models.OneToOneField('circulation.Loan')

    return_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} [return: {}]".format(self.loan, self.return_at.date())
