from django.db import models
from django.conf import settings

from django_countries import fields as dj_countries_fields

from registration import signals


class MembershipType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    membership_type = models.ForeignKey('MembershipType')
    patron = models.ForeignKey('Patron')

    register_on = models.DateField(blank=True, null=True)
    expire_on = models.DateField(blank=True, null=True)

    # timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} [{}]".format(self.patron, self.membership_type)


class IdentificationType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class PatronIdentification(models.Model):
    patron = models.ForeignKey('Patron')
    id_type = models.ForeignKey('IdentificationType')
    value = models.CharField(max_length=60)

    def __str__(self):
        return "{}:{}".format(self.id_type, self.value)

class Patron(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    birth_date = models.DateField(blank=True, null=True)

    address = models.TextField(blank=True)
    country = dj_countries_fields.CountryField()
    postcode = models.CharField(max_length=12, blank=True)
    contact = models.CharField(max_length=30, blank=True)

    note = models.TextField(blank=True,
            help_text='Extra Information for Administrator')

    notification_type = models.CharField(max_length=25, blank=True)

    # Loan duration (in days unit)
    loan_duration = models.IntegerField(default=15)

    # Maximum concurrent resource loaned
    loan_limit = models.IntegerField(default=2)

    # Maximum renewal for each items
    renewal_limit = models.IntegerField(default=3)

    def __str__(self):
        return self.user.username

    def get_loan_duration(self):
        # TODO: Implement a strategy where by default loan duration is null
        # and when it is null, it will determine
        # the limit by the patron membership
        # Special consideration for different type of resources
        # may have different loan duration
        return self.loan_duration

    def get_loan_limit(self):
        # TODO: Implement a strategy where by default loan limit is null
        # and when it is null, it will determine
        # the limit by the patron membership
        # Special consideration for different type of resources
        # may have different loan limit
        """
        TODO: loan limit is determined by:
        - patron membership (limit generalization)
        --> which specifies limit for different resource type
        --> and specifies its default limit as fallback type
        - patron: (specific limit overwrite)
        --> patron limit takes highest priority
        --> different types of resources has different overwrite.
        """
        return self.loan_limit

    def get_renewal_limit(self):
        # TODO: Implement a strategy where by default renewal limit is null
        # and when it is null, it will determine
        # the limit by the patron membership
        return self.renewal_limit

def create_patron(sender, **kwargs):
    patron = Patron(user=kwargs.get('user'))
    patron.save()

signals.user_registered.connect(create_patron)
