from django import forms
from django.utils.translation import ugettext_lazy as _

from .. import models as catalog_models


class BaseResourceForm(forms.ModelForm):
    subtitle = forms.CharField()
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
        model = catalog_models.Book
        fields = [
            'title', 'subtitle',
            'agents', 'subjects', 'classifications',
        ]


class LookupForm(forms.Form):
    bibtype = forms.ModelChoiceField(
            queryset=catalog_models.BookIdentifierType.objects.all(),
            initial=0)
    bibvalue = forms.CharField()
