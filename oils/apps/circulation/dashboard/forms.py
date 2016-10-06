from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()

from .. import models
from .. import get_backend
from oils.apps.catalog import models as catalog_models
from oils.apps.patron import models as patron_models
from oils.apps.holding import models as holding_models


class LoanCreateForm(forms.Form):
    item = forms.ModelChoiceField(
            widget=forms.TextInput(),
            label=_("Item Code"),
            queryset=holding_models.Item.objects.all(),
            to_field_name='code',
            error_messages={
                'invalid_choice': 'One or more of the items is unavailable'
            })
    patron = forms.ModelChoiceField(
            widget=forms.TextInput(),
            label=_("Patron Username"),
            queryset=User.objects.filter(patron__isnull=False),
            to_field_name='username')


    def clean(self):
        data = super().clean()
        try:
            inst = models.Loan(patron=data['patron'].patron, item=data['item'])
        except KeyError:
            return data
        try:
            inst.clean()
        except models.ValidationError as e:
            raise forms.ValidationError(e.message_dict, code='invalid')
        return data
        
class LoanRenewalForm(forms.Form):
    resource_code = forms.ModelChoiceField(
            widget=forms.TextInput(),
            label=_("Resource Code"),
            queryset=holding_models.Item.objects.all(),
            to_field_name='code',
            error_messages={
                'invalid_choice': 'One or more of the resources is unavailable'
            })

    def clean(self):
        backend = get_backend()
        cleaned_data = super().clean()
        for item in cleaned_data['resource_code']:
            for loan in item.loan_set.all():
                backend.validate(loan)
        return cleaned_data



class LoanReturnForm(forms.Form):
    resource_code = forms.ModelChoiceField(
            widget=forms.TextInput(),
            label=_("Resource Code"),
            queryset=holding_models.Item.objects.all(),
            to_field_name='code',
            error_messages={
                'invalid_choice': 'One or more of the resources is unavailable'
            })
