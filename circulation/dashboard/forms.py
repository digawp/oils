from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import models as auth_models

from circulation import models
from circulation import get_backend
from catalogue import models as catalogue_models
from patron import models as patron_models


class ReactSelectModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def _check_values(self, value):
        if value:
            value = value[0].split(',')
        return super()._check_values(value)

class IssueCreateForm(forms.Form):
    resource_code = ReactSelectModelMultipleChoiceField(
            label=_("Resource Code"),
            queryset=catalogue_models.ResourceInstance.objects.available(),
            to_field_name='code',
            error_messages={
                'invalid_choice': 'One or more of the resources is unavailable'
            })
    patron_username = forms.ModelChoiceField(
            label=_("Patron Username"),
            queryset=auth_models.User.objects.filter(patron__isnull=False),
            to_field_name='username')


class IssueRenewalForm(forms.Form):
    resource_code = ReactSelectModelMultipleChoiceField(
            label=_("Resource Code"),
            queryset=catalogue_models.ResourceInstance.objects.all(),
            to_field_name='code')

    def clean(self):
        backend = get_backend()
        cleaned_data = super().clean()
        for resource_instance in cleaned_data['resource_code']:
            for issue in resource_instance.issue_set.all():
                backend.validate(issue)
        return cleaned_data



class IssueReturnForm(forms.Form):
    resource_code = ReactSelectModelMultipleChoiceField(
            label=_("Resource Code"),
            queryset=catalogue_models.ResourceInstance.objects.all(),
            to_field_name='code')
