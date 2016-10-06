from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from django.views import generic
from django.db.models import F

import django_tables2 as tables2

from . import tables
from . import forms
from .. import models

from oils.apps.dashboard import mixins


class PatronIndexView(
        mixins.DashboardContextMixin,
        tables2.SingleTableMixin,
        generic.ListView):
    model = models.Patron
    template_name = 'patron/dashboard/index.html'
    table_class = tables.PatronTable
    context_table_name = 'patron_table'
    table_pagination = {
        'per_page': 20,
    }

    def get_table_data(self):
        patrons = super().get_table_data()
        return patrons.annotate(
                username=F('user__username'),
                email=F('user__email'),
                firstname=F('user__first_name'),
                lastname=F('user__last_name'),
                is_active=F('user__is_active'),
        ).values('pk', 'username', 'email', 'firstname', 'lastname', 'loan_limit', 'is_active')


class PatronActivationView(
        mixins.DashboardContextMixin,
        generic.detail.SingleObjectMixin,
        generic.View):
    model = models.Patron

    def post(self, *args, **kwargs):
        user = self.get_object().user
        if self.kwargs['activate']:
            user.is_active = True
        else:
            user.is_active = False
        user.save()
        return redirect(reverse('dashboard:patron:index'))

class PatronRegistrationView(
        mixins.DashboardContextMixin,
        generic.FormView):
    """Patron Registration made by the Staff"""
    template_name = 'patron/dashboard/patron_registration.html'
    form_class = forms.PatronRegistrationForm

    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:patron:index')

    def form_valid(self, form):
        # TODO: Save Patron
        return super().form_valid(form)
