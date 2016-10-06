from django.shortcuts import render
from django.views import generic
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Count, Max

import django_tables2 as tables2

from .. import models as circulation_models

from . import tables
from . import forms

from oils.apps.dashboard import mixins as dashboard_mixins


class OneStopView(
        dashboard_mixins.DashboardContextMixin,
        generic.TemplateView):
    template_name = 'circulation/dashboard/onestop.html'


class LoanIndexView(
        dashboard_mixins.DashboardContextMixin,
        tables2.SingleTableMixin,
        generic.ListView):
    template_name = 'circulation/dashboard/index.html'
    model = circulation_models.Loan
    table_class = tables.LoanTable
    context_table_name = 'loan_table'
    table_pagination = {
        'per_page': 10,
    }
    
    def get_queryset(self):
        qs = super().get_queryset()
        onloan = qs.filter(loanreturn__isnull=True)
        if self.request.user.is_staff:
            return onloan
        else:
            return onloan.filter(
                    patron=self.request.user.patron)

    def get_table_data(self):
        return super().get_table_data().annotate(
            total_renewal=Count('loanrenewal'),
            last_renewal=Max('loanrenewal__renew_at'),
        )

class LoanSuccessView(
        dashboard_mixins.DashboardContextMixin,
        generic.TemplateView):
    template_name = 'circulation/dashboard/loan_success.html'

class LoanRenewalView(
        dashboard_mixins.DashboardContextMixin,
        generic.FormView):
    template_name = 'circulation/dashboard/loanrenewal_create.html'
    form_class = forms.LoanRenewalForm

    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:circulation:loan:success')

    def form_valid(self, form):
        form.cleaned_data['item'].loan_set.last().renew()
        return super().form_valid(form)

class LoanReturnView(
        dashboard_mixins.DashboardContextMixin,
        generic.FormView):
    template_name = 'circulation/dashboard/loanreturn_create.html'
    form_class = forms.LoanReturnForm

    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:circulation:loan:index')

    def form_valid(self, form):
        circulation_models.LoanReturn.objects.create(
                loan=form.cleaned_data['item'].loan_set.last())
        return super().form_valid(form)

class LoanDeleteView(
        dashboard_mixins.DashboardContextMixin,
        generic.DeleteView):
    template_name = 'circulation/dashboard/loan_delete.html'
    model = circulation_models.Loan

class LoanReturnDeleteView(
        dashboard_mixins.DashboardContextMixin,
        generic.DeleteView):
    template_name = 'circulation/dashboard/loanreturn_delete.html'
    model = circulation_models.LoanReturn

class LoanCreateView(
        dashboard_mixins.DashboardContextMixin,
        generic.FormView):
    template_name = 'circulation/dashboard/loan_create.html'
    form_class = forms.LoanCreateForm
    
    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:circulation:loan:success')

    def form_valid(self, form):
        circulation_models.Loan.objects.create(
                item=form.cleaned_data['item'],
                patron=form.cleaned_data['patron'].patron)
        return super().form_valid(form)

class CirculationIndexRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse('dashboard:circulation:loan:onestop')
