from django import forms
from django.utils.translation import ugettext_lazy as _

from circulation import models

class IssueCreateForm(forms.ModelForm):
    resource_identifier = forms.CharField(label=_("Resource Code"))
    patron_id = forms.CharField(label=_("Patron ID"))

    class Meta:
        model = models.Issue
        fields = ('resource_identifier', 'patron_id') 
