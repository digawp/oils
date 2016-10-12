from django import forms

import django_countries as dj_countries
from .. import models

NOTIFICATION_CHOICES =(
    (1, 'SMS'),
    (2, 'Email'),
    (4, 'Post Mail'),
)

class IdentificationWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        _widgets = (
            forms.Select(attrs=attrs),
            forms.TextInput(attrs=attrs)
        )
        super().__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.id_type, value.value]
        return [None, None]

class IdentificationField(forms.MultiValueField):
    widget = IdentificationWidget

    def __init__(self, *args, **kwargs):
        _fields = (
            forms.ModelChoiceField(queryset=models.IdentificationType.objects.all(), initial=0),
            forms.CharField()
        )
        super().__init__(_fields, *args, **kwargs)
        self.widget.widgets[0].choices = self.fields[0].widget.choices

    def compress(self, data_list):
        if data_list:
            if data_list[0] in self.empty_values:
                raise ValidationError("Choose the ID Type", code='invalid_idtype')
            if data_list[1] in self.empty_values:
                raise ValidationError("Enter the ID Number", code='invalid_idvalue')
            return models.PatronIdentification(
                    id_type=data_list[0],
                    value=data_list[1])
        return None


class PatronRegistrationForm(forms.Form):
    identification = IdentificationField()
    username = forms.CharField(help_text="User's login name")
    membership_type = forms.ModelChoiceField(
            models.MembershipType.objects.all())

    # Extra Info Section
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    birth_date = forms.DateField(required=False)
    notification_type = forms.TypedMultipleChoiceField(
            coerce=int,
            choices=NOTIFICATION_CHOICES,
            initial=[1,2,4],
            widget=forms.CheckboxSelectMultiple,
            required=False)

    # Loan Control Section
    loan_duration = forms.IntegerField(min_value=0, initial=0)
    loan_limit = forms.IntegerField(min_value=0, initial=0)
    renewal_limit = forms.IntegerField(min_value=0, initial=0)

    # Address Section
    address = forms.CharField(required=False, widget=forms.Textarea)
    country = dj_countries.fields.LazyTypedChoiceField(
            required=False,
            initial='SG',
            choices=[('', '-----')]+list(dj_countries.countries))
    postcode = forms.CharField(required=False)
    contact = forms.CharField(required=False)

    # Admin Section
    note = forms.CharField(required=False, widget=forms.Textarea)

