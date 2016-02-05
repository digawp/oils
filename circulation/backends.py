from django.utils import timezone
from . import models

from datetime import timedelta

from . import exceptions


class RenewalBackend(object):
    def _validate_renewal_limit(self, issue):
        issue_renewal_count = models.IssueRenewal.objects.filter(
                issue=issue).count()
        patron_renewal_limit = issue.patron.get_renewal_limit()
        if (issue_renewal_count >= patron_renewal_limit):
            raise exceptions.RenewalLimitException(
                "Patron has reach the current loan limit")

    def validate(self, issue):
        self._validate_renewal_limit(issue)
        

    def renew(self, issue):
        raise NotImplementedError("Renewal Backend is not well defined")

class RenewalFromDue(RenewalBackend):
    def renew(self, issue):
        loan_duration = issue.patron.get_loan_duration()

        last_renewal = models.IssueRenewal.objects.get_last_renewal(
                issue=issue)
        if not last_renewal:
            last_loan_at = issue.loan_at
        else:
            last_loan_at = last_renewal.renew_at
        renewal_start_at = last_loan_at + timedelta(days=loan_duration)
        return models.IssueRenewal.objects.create(
            issue=issue, renew_at=renewal_start_at)


class RenewalFromToday(RenewalBackend):
    def renew(self, issue):
        return models.IssueRenewal.objects.create(
            issue=issue, renew_at=timezone.now())
