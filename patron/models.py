from django.db import models

from registration import signals


class Patron(models.Model):
    user = models.OneToOneField('auth.User')

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
