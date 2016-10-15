from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.contenttypes import fields as ct_fields
from django.contrib.contenttypes import models as ct_models

from datetime import datetime, timedelta


from . import get_backend
from . import exceptions

from oils.apps.holding import models as holding_models
from oils.apps.patron import models as patron_models

DEFAULT_LOAN_LIMIT = settings.OILS['CIRCULATION'].get('DEFAULT_LOAN_LIMIT', 8)
DEFAULT_LOAN_DURATION = settings.OILS['CIRCULATION'].get('DEFAULT_LOAN_DURATION', 20)
DEFAULT_RENEWAL_LIMIT = settings.OILS['CIRCULATION'].get('DEFAULT_RENEWAL_LIMIT', 3)

class BorrowingPrivillage(models.Model):
    loan_limit = models.IntegerField(default=DEFAULT_LOAN_LIMIT)
    loan_duration = models.IntegerField(default=DEFAULT_LOAN_DURATION)
    renewal_limit = models.IntegerField(default=DEFAULT_RENEWAL_LIMIT)

    membership_type = models.OneToOneField(patron_models.MembershipType)

def create_borrowing_privillage(sender, instance, created, **kwargs):
    try:
        instance.borrowingprivillage
    except BorrowingPrivillage.DoesNotExist:
        BorrowingPrivillage.objects.create(membership_type=instance)

post_save.connect(create_borrowing_privillage, sender=patron_models.MembershipType)

class LoanRenewalManager(models.Manager):
    def get_last_renewal(self, loan):
        return self.filter(loan=loan).order_by('renew_at').last()

class LoanManager(models.Manager):
    def create_loan(self, patron, *args, **kwargs):
        if not self.last().is_returned:
            raise ValueError("Resource has not been returned")
        return self.create(item=self.item, 
            patron=patron, *args, **kwargs)


class ClosedLoanManager(models.Manager):
    """Historical Loan records that has been returned"""
    def get_queryset(self):
        return super().get_queryset().filter(loanreturn__isnull=False)

class OpenedLoanManager(models.Manager):
    """Loan records that has not yet been returned"""
    def get_queryset(self):
        return super().get_queryset().filter(loanreturn__isnull=True)

def get_due_date():
    return datetime.now() + timedelta(days=20)

class Loan(models.Model):
    item = models.ForeignKey('holding.Item')
    patron = models.ForeignKey('patron.Patron')
    loan_at = models.DateTimeField(auto_now_add=True)
    due_on = models.DateField(default=get_due_date)

    objects = LoanManager()
    closes = ClosedLoanManager()
    opens = OpenedLoanManager()

    def __str__(self):
        data = {
            'item': self.item.resource_identifiers,
            'loan_date': self.loan_at.date(),
            'borrower': self.patron
        }
        return "[{item}] [borrow: {loan_date} by {borrower}]".format(**data)

    @property
    def is_returned(self):
        if self.pk: #  Existing Loan (check the loan return record)
            try:
                return self.loanreturn is not None
            except ObjectDoesNotExist:
                return False
        else: # New Loan (check the resource)
            last_loan = Loan.objects.filter(item=self.item).last()
            if last_loan:
                try:
                    return last_loan.is_returned
                except ObjectDoesNotExist:
                    return False
            return True

    def renew(self):
        backend = get_backend()
        return backend.renew(loan=self)


    def clean_patron(self):

        if Loan.opens.filter(patron=self.patron).count() >= self.patron.loan_limit:
            raise ValidationError({
                'patron': 'Patron has exceed the loan limit',
            })

    def clean_item(self):
        if self.item and not self.is_returned:
            raise ValidationError({
                'item': 'Item is not available'
            })

    def clean(self):
        self.clean_patron()
        self.clean_item()

class LoanRenewal(models.Model):
    loan = models.ForeignKey('Loan')

    renew_at = models.DateTimeField()

    objects = LoanRenewalManager()

    def __str__(self):
        return "{} [extend: {}]".format(self.loan, self.renew_at.date())

    def clean(self):
        if self.loan_id:
            backend = get_backend()
            try:
                backend.validate(self.loan)
            except exceptions.RenewalLimitException as e:
                raise exceptions.RenewalLimitException({'loan': e.message})


class LoanReturn(models.Model):
    loan = models.OneToOneField('circulation.Loan')

    return_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} [return: {}]".format(self.loan, self.return_at.date())
