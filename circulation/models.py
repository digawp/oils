from django.db import models
from django.contrib.contenttypes import fields as ct_fields
from django.contrib.contenttypes import models as ct_models


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


class IssueRenewal(models.Model):
    issue = models.ForeignKey('Issue')

    renew_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} [extend: {}]".format(self.issue, self.renew_at.date())


class IssueReturn(models.Model):
    issue = models.OneToOneField('circulation.Issue')

    return_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} [return: {}]".format(self.issue, self.return_at.date())
