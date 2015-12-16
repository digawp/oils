from django import forms
from django.utils.translation import ugettext_lazy as _

from catalogue import models as catalogue_models


class ResourceInstanceForm(forms.ModelForm):
    class Meta:
        model = catalogue_models.ResourceInstance
        fields = [
            'code',
            'creative_work_type',
            'creative_work_id',
        ]


class ResourceTypeSelectForm(forms.Form):
    resource_type = forms.ModelChoiceField(
        label=_('Create a new resource of type'),
        empty_label=_('Book'),
        queryset=catalogue_models.SerialType.objects.all())


class BookForm(forms.ModelForm):
    class Meta:
        model = catalogue_models.Book
        fields = [
            'isbn13', 'title', 'subtitle', 'abstract',
        ]

class SerialForm(forms.ModelForm):
    class Meta:
        model = catalogue_models.Serial
        fields = [
            'issn', 'title', 'subtitle', 'abstract',
        ]
