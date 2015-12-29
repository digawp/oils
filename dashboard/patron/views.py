from django.shortcuts import render

from django.views import generic
from django.db.models import F

import django_tables2 as tables2

from . import tables
from . import forms
from patron import models

# Create your views here.

class PatronIndexView(tables2.SingleTableMixin, generic.ListView):
    model = models.Patron
    template_name = 'dashboard/patron/index.html'
    table_class = tables.PatronTable
    context_table_name = 'patron_table'
    table_pagination = {
        'per_page': 20,
    }

    def get_table_data(self):
        patrons = self.get_queryset()
        return patrons.annotate(
                username=F('user__username'),
                email=F('user__email'),
                firstname=F('user__first_name'),
                lastname=F('user__last_name')
        ).values('username', 'email', 'firstname', 'lastname', 'loan_limit')
