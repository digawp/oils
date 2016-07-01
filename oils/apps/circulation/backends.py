from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from . import models

from datetime import timedelta

from . import exceptions


class RenewalBackend(object):
    def _validate_resource_not_returned(self, loan):
        try:
            loanreturn = loan.loanreturn
        except ObjectDoesNotExist:
            pass
        else:
            raise ValidationError({'renew_at': 'Loan has been returned'})

    def _validate_renewal_limit(self, loan):
        loan_renewal_count = models.LoanRenewal.objects.filter(
                loan=loan).count()
        patron_renewal_limit = loan.patron.get_renewal_limit()
        if (loan_renewal_count >= patron_renewal_limit):
            raise exceptions.RenewalLimitException(
                "Patron has reach the current loan limit")

    def validate(self, loan):
        self._validate_resource_not_returned(loan)
        self._validate_renewal_limit(loan)
        

    def renew(self, loan):
        raise NotImplementedError("Renewal Backend is not well defined")

class RenewalFromDue(RenewalBackend):
    def renew(self, loan):
        loan_duration = loan.patron.get_loan_duration()

        last_renewal = models.LoanRenewal.objects.get_last_renewal(
                loan=loan)
        if not last_renewal:
            last_loan_at = loan.loan_at
        else:
            last_loan_at = last_renewal.renew_at
        renewal_start_at = last_loan_at + timedelta(days=loan_duration)
        return models.LoanRenewal.objects.create(
            loan=loan, renew_at=renewal_start_at)


class RenewalFromToday(RenewalBackend):
    def renew(self, loan):
        return models.LoanRenewal.objects.create(
            loan=loan, renew_at=timezone.now())
