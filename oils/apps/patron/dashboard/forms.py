from django import forms

class PatronRegistrationForm(forms.Form):
    username = forms.CharField()
    identification = forms.CharField()
