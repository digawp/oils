from django.core.exceptions import ValidationError


class RenewalLimitException(ValidationError):
    pass
