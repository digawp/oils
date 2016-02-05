from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes import fields as ct_fields
from django.contrib.contenttypes import models as ct_models


from . import get_backend


class IssueRenewalManager(models.Manager):
    def get_last_renewal(self, issue):
        return self.filter(issue=issue).order_by('renew_at').last()


class Issue(models.Model):
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
        backend.renew(issue=self)


class IssueRenewal(models.Model):
    issue = models.ForeignKey('Issue')

    renew_at = models.DateTimeField()

    objects = IssueRenewalManager()

    def __str__(self):
        return "{} [extend: {}]".format(self.issue, self.renew_at.date())

    def clean(self):
        backend = get_backend()
        backend.validate(self.issue)


class IssueReturn(models.Model):
    issue = models.OneToOneField('circulation.Issue')

    return_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} [return: {}]".format(self.issue, self.return_at.date())
