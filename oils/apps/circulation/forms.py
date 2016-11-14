from django import forms

from . import models

class LoanForm(forms.ModelForm):
    class Meta:
        model = models.Loan
        fields = ('item', 'patron',)

class LoanRenewalForm(forms.ModelForm):
    class Meta:
        model = models.LoanRenewal
        fields = ('loan',)


class LoanReturnForm(forms.ModelForm):
    class Meta:
        model = models.LoanReturn
        fields = ('loan',)
