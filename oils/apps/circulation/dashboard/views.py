from django.shortcuts import render
from django.views import generic
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Count, Max
from django.contrib import messages
from django.utils.safestring import mark_safe

import django_tables2 as tables2

from .. import models as circulation_models

from . import tables
from . import forms

from oils.apps.dashboard import mixins as dashboard_mixins



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
        qs = qs.filter(loanreturn__isnull=True)
        if not self.request.user.is_staff:
            qs = onloan.filter(
                    patron=self.request.user.patron)
        return qs

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
    success_message = """
    Book "{title}" has been renewed.
    <a href="{link}">More Info.</a>
    """
    
    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:circulation:loan:renewal')

    def get_success_message(self, cleaned_data):
        return mark_safe(self.success_message.format(**{
            'title': cleaned_data['item'].book.title,
            'link': reverse('dashboard:circulation:loan:success'),
        }))

    def form_valid(self, form):
        form.cleaned_data['item'].loan_set.last().renew()
        messages.success(self.request, self.get_success_message(form.cleaned_data))
        return super().form_valid(form)

class LoanReturnView(
        dashboard_mixins.DashboardContextMixin,
        generic.FormView):
    template_name = 'circulation/dashboard/loanreturn_create.html'
    form_class = forms.LoanReturnForm
    success_message = """
    Book "{title}" has been returned.
    <a href="{link}">More Info.</a>
    """
    
    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:circulation:loan:return')

    def get_success_message(self, cleaned_data):
        return mark_safe(self.success_message.format(**{
            'title': cleaned_data['item'].book.title,
            'link': reverse('dashboard:circulation:loan:success'),
        }))

    def form_valid(self, form):
        circulation_models.LoanReturn.objects.create(
                loan=form.cleaned_data['item'].loan_set.last())
        messages.success(self.request, self.get_success_message(form.cleaned_data))
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
    form_class = forms.LoanForm
    success_message = """
    Loan successful for {patron} on [{titles}] until {due:%d-%b-%Y}.
    <a href="{link}">More Info.</a>
    """
    
    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:circulation:loan:new')

    def get_success_message(self, cleaned_data):
        return mark_safe(self.success_message.format(**{
            'patron': cleaned_data['patron'].get_full_name(),
            'titles': ','.join(
                loan.item.book.title for loan in cleaned_data['loans']),
            'due': cleaned_data['loans'][0].due_on,
            'link': reverse('dashboard:circulation:loan:success'),
        }))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = forms.LoanFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        return self.form_invalid(form, formset)


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if 'formset' not in kwargs:
            ctx['formset'] = forms.LoanFormSet()
        return ctx

    def form_valid(self, form, formset):
        formset.instance = form.cleaned_data['patron'].patron
        loan_set = formset.save()
        success_message = self.get_success_message(
                dict(form.cleaned_data, loans=loan_set))
        messages.success(self.request, success_message)
        return super().form_valid(form)

    def form_invalid(self, form, formset):
        ctx = self.get_context_data(form=form, formset=formset)
        return self.render_to_response(ctx)

class CirculationIndexRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse('dashboard:circulation:loan:index')
