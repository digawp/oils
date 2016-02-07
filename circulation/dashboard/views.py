from django.shortcuts import render
from django.views import generic
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Count, Max

import django_tables2 as tables2

from circulation import models as circulation_models

from . import tables
from . import forms



class IssueIndexView(tables2.SingleTableMixin, generic.ListView):
    template_name = 'circulation/dashboard/index.html'
    model = circulation_models.Issue
    table_class = tables.IssueTable
    context_table_name = 'issue_table'
    table_pagination = {
        'per_page': 10,
    }
    
    def get_queryset(self):
        qs = super().get_queryset()
        onloan = qs.filter(issuereturn__isnull=True)
        if self.request.user.is_staff:
            return onloan
        else:
            return onloan.filter(
                    patron=self.request.user.patron)

    def get_table_data(self):
        return super().get_table_data().annotate(
            total_renewal=Count('issuerenewal'),
            last_renewal=Max('issuerenewal__renew_at'),
        )


class IssueRenewalView(generic.FormView):
    template_name = 'circulation/dashboard/issuerenewal_create.html'
    form_class = forms.IssueRenewalForm

    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:circulation:index')

    def form_valid(self, form):
        for resource_instance in form.cleaned_data['resource_code']:
            resource_instance.issue_set.last().renew()
        return super().form_valid(form)

class IssueReturnView(generic.FormView):
    template_name = 'circulation/dashboard/issuereturn_create.html'
    form_class = forms.IssueReturnForm

    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:circulation:index')

    def form_valid(self, form):
        for resource_instance in form.cleaned_data['resource_code']:
            circulation_models.IssueReturn.objects.create(
                    issue=resource_instance.issue_set.last())
        return super().form_valid(form)

class IssueDeleteView(generic.DeleteView):
    template_name = 'circulation/dashboard/issue_delete.html'
    model = circulation_models.Issue

class IssueReturnDeleteView(generic.DeleteView):
    template_name = 'circulation/dashboard/issuereturn_delete.html'
    model = circulation_models.IssueReturn

class IssueCreateView(generic.FormView):
    template_name = 'circulation/dashboard/issue_create.html'
    form_class = forms.IssueCreateForm
    
    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:circulation:index')

    def form_valid(self, form):
        for resource_instance in form.cleaned_data['resource_code']:
            circulation_models.Issue.objects.create(
                    resource=resource_instance,
                    patron=form.cleaned_data['patron_username'].patron)
        return super().form_valid(form)

class CirculationIndexRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse('dashboard:circulation:issue:index')
