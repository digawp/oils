from django.shortcuts import render
from django.views import generic
from django.core.urlresolvers import reverse

import django_tables2 as tables2

from circulation import models as circulation_models

from . import tables
from . import forms



class IssueIndexView(tables2.SingleTableMixin, generic.ListView):
    template_name = 'dashboard/circulation/index.html'
    model = circulation_models.Issue
    table_class = tables.IssueTable
    context_table_name = 'issue_table'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(
                    patron=self.request.user.patron)


class IssueRenewalView(generic.CreateView):
    template_name = 'dashboard/circulation/issue_renewal_create.html'
    model = circulation_models.IssueRenewal

class IssueReturnView(generic.CreateView):
    template_name = 'dashboard/circulation/issue_return_create.html'
    model = circulation_models.IssueReturn

class IssueDeleteView(generic.DeleteView):
    template_name = 'dashboard/circulation/issue_delete.html'
    model = circulation_models.Issue

class IssueReturnDeleteView(generic.DeleteView):
    template_name = 'dashboard/circulation/issue_return_delete.html'
    model = circulation_models.IssueReturn

class IssueCreateView(generic.CreateView):
    template_name = 'dashboard/circulation/issue_create.html'
    model = circulation_models.Issue
    form_class = forms.IssueCreateForm

class CirculationIndexRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse('dashboard:circulation:issue:index')
