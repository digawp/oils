from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import models as auth_models

from .. import models
from .. import get_backend
from oils.apps.catalog import models as catalog_models
from oils.apps.patron import models as patron_models
from oils.apps.holding import models as holding_models


class ReactSelectModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def _check_values(self, value):
        if value:
            value = value[0].split(',')
        return super()._check_values(value)

class LoanCreateForm(forms.Form):
    resource_code = ReactSelectModelMultipleChoiceField(
            label=_("Resource Code"),
            queryset=holding_models.Item.objects.all(),
            to_field_name='code',
            error_messages={
                'invalid_choice': 'One or more of the resources is unavailable'
            })
    patron_username = forms.ModelChoiceField(
            label=_("Patron Username"),
            queryset=auth_models.User.objects.filter(patron__isnull=False),
            to_field_name='username')


class LoanRenewalForm(forms.Form):
    resource_code = ReactSelectModelMultipleChoiceField(
            label=_("Resource Code"),
            queryset=holding_models.Item.objects.all(),
            to_field_name='code')

    def clean(self):
        backend = get_backend()
        cleaned_data = super().clean()
        for item in cleaned_data['resource_code']:
            for loan in item.loan_set.all():
                backend.validate(loan)
        return cleaned_data



class LoanReturnForm(forms.Form):
    resource_code = ReactSelectModelMultipleChoiceField(
            label=_("Resource Code"),
            queryset=holding_models.Item.objects.all(),
            to_field_name='code')
