from functools import reduce
from operator import ior
from django import forms
from django.contrib.auth import get_user_model
from django.forms import ValidationError

User = get_user_model()

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
            return [value.id_type.pk, value.value]
        return [None, None]

class IdentificationField(forms.MultiValueField):
    widget = IdentificationWidget

    def __init__(self, *args, **kwargs):
        _fields = (
            forms.ModelChoiceField(queryset=models.IdentificationType.objects.all()),
            forms.CharField()
        )
        super().__init__(_fields, *args, **kwargs)
        self.widget.widgets[0].choices = self.fields[0].widget.choices

    def compress(self, data_list):
        if data_list:
            if data_list[0] in self.empty_values:
                # raise ValidationError("Choose the ID Type", code='invalid_idtype')
                return None
            if data_list[1] in self.empty_values:
                # raise ValidationError("Enter the ID Number", code='invalid_idvalue')
                return None
            return models.PatronIdentification(
                    id_type=data_list[0],
                    value=data_list[1])
        return None


class PatronRegistrationForm(forms.Form):
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

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = (
                'username', 'email',
                'first_name', 'last_name', 
        )

class NotificationTypeField(forms.TypedMultipleChoiceField):
    def prepare_value(self, value):
        if isinstance(value, int):
            check_value = []
            for choice, _ in NOTIFICATION_CHOICES:
                if choice & value != 0:
                    check_value.append(choice)
            return check_value
        elif isinstance(value, list):
            value = [int(v) for v in value]
            return self.prepare_value(reduce(ior, value))

class PatronCreateForm(forms.ModelForm):
    membership_type = forms.ModelChoiceField(
            models.MembershipType.objects.all())
    notification_type = NotificationTypeField(
            coerce=int,
            choices=NOTIFICATION_CHOICES,
            initial=[1,2,4],
            widget=forms.CheckboxSelectMultiple,
            required=False)
    class Meta:
        model = models.Patron
        fields = (
                'membership_type',
                'loan_duration', 'loan_limit', 'renewal_limit',
                'notification_type',
                'birth_date', 
                'address', 'country', 'postcode', 'contact', 
                'note',)


    def clean_notification_type(self):
        return reduce(ior, self.cleaned_data['notification_type'])

class PatronUpdateForm(forms.ModelForm):
    """
    Changing membership is not allowed.
    """
    notification_type = NotificationTypeField(
            coerce=int,
            choices=NOTIFICATION_CHOICES,
            initial=[1,2,4],
            widget=forms.CheckboxSelectMultiple,
            required=False)
    class Meta:
        model = models.Patron
        fields = (
                'loan_duration', 'loan_limit', 'renewal_limit',
                'notification_type',
                'birth_date', 
                'address', 'country', 'postcode', 'contact', 
                'note',)


    def clean_notification_type(self):
        return reduce(ior, self.cleaned_data['notification_type'])
        

class PatronIdentificationForm(forms.ModelForm):
    identification = IdentificationField(required=False)

    class Meta:
        model = models.PatronIdentification
        fields = ['identification']

    def __init__(self, *args, **kwargs):
        kwargs['initial'] = {
            'identification': kwargs.get('instance')
        }
        super().__init__(*args, **kwargs)

    def clean_identification(self):
        data = self.cleaned_data['identification']
        return data

    def save(self, commit=True):
        patron_identification = super().save(commit)
        patron_identification.id_type = self.cleaned_data['identification'].id_type
        patron_identification.value = self.cleaned_data['identification'].value
        if commit:
            patron_identification.save()
        return patron_identification


PatronIdentificationFormSet = forms.inlineformset_factory(
        models.Patron, models.PatronIdentification, fields=['identification'],
        form=PatronIdentificationForm,
        min_num=1, extra=1, validate_min=True)
