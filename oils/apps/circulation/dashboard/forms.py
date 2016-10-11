from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
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

class LoanForm(forms.Form):
    patron = forms.ModelChoiceField(
            widget=forms.TextInput(),
            label=_("Patron"),
            queryset=User.objects.filter(patron__isnull=False),
            to_field_name='username')

    def clean_patron(self):
        user = self.cleaned_data['patron']
        try:
            models.Loan(patron=user.patron).clean_patron()
        except models.ValidationError as e:
            raise forms.ValidationError(e.message_dict['patron'], code='invalid')
        return user


class LoanItemBaseForm(forms.ModelForm):
    item = forms.ModelChoiceField(
            widget=forms.TextInput(),
            label=_("Item Code"),
            queryset=holding_models.Item.objects.all(),
            to_field_name='code')


LoanFormSet = forms.inlineformset_factory(
        patron_models.Patron, models.Loan, fields=('item',),
        form=LoanItemBaseForm,
        widgets={'item': forms.TextInput()},
        min_num=1, validate_min=True, extra=3)
        
class LoanRenewalForm(forms.Form):
    item_code = forms.ModelChoiceField(
            widget=forms.TextInput(),
            label=_("Item Code"),
            queryset=holding_models.Item.objects.filter(loan__in=models.Loan.opens.all()),
            to_field_name='code',
            error_messages={
                'invalid_choice': 'This item is not being loaned out'
            })


    def clean(self):
        backend = get_backend()
        cleaned_data = super().clean()
        item = cleaned_data['item_code']
        last_loan = item.loan_set.last()
        backend.validate(last_loan)
        return cleaned_data


class LoanReturnForm(forms.Form):
    item = forms.ModelChoiceField(
            widget=forms.TextInput(),
            label=_("Item Code"),
            queryset=holding_models.Item.objects.filter(loan__in=models.Loan.opens.all()),
            to_field_name='code',
            error_messages={
                'invalid_choice': 'This item is not being loaned out'
            })


