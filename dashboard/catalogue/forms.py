from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic as ct_generic

from catalogue import models as catalogue_models


class ResourceInstanceForm(forms.ModelForm):
    class Meta:
        model = catalogue_models.ResourceInstance
        fields = [
            'code',
            'creative_work_type',
            'creative_work_id',
        ]

ResourceInstanceFormSet = ct_generic.generic_inlineformset_factory(
    catalogue_models.ResourceInstance, **{
        'form': ResourceInstanceForm,
        'ct_field': 'creative_work_type',
        'fk_field': 'creative_work_id',
    })

class ResourceTypeSelectForm(forms.Form):
    resource_type = forms.ModelChoiceField(
        label=_('Create a new resource of type'),
        empty_label=_('Book'),
        queryset=catalogue_models.SerialType.objects.all())


class BaseResourceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['title'].widget.attrs['readonly'] = True
            self.fields['subtitle'].widget.attrs['readonly'] = True
            self.fields['abstract'].widget.attrs['readonly'] = True

    def clean_title(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.title
        else:
            return self.cleaned_data['title']

    def clean_subtitle(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.subtitle
        else:
            return self.cleaned_data['subtitle']

    def clean_abstract(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.abstract
        else:
            return self.cleaned_data['abstract']


class BookForm(BaseResourceForm):
    class Meta:
        model = catalogue_models.Book
        fields = [
            'isbn13', 'title', 'subtitle', 'abstract', 'publisher',
            'authors', 'subjects',
        ]


class SerialForm(forms.ModelForm):
    class Meta:
        model = catalogue_models.Serial
        fields = [
            'issn', 'title', 'subtitle', 'abstract', 'publisher',
            'authors', 'subjects',
        ]
