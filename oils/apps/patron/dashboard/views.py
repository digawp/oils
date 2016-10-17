from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.db.models.functions import Concat
from django.db.models import Value as V
from functools import reduce
import operator

from django.views import generic
from django.db.models import F
from django.contrib.auth import get_user_model
User = get_user_model()

import django_tables2 as tables2
from registration.signals import user_registered

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
                name=Concat('user__first_name', V(' '), 'user__last_name'),
                datejoin=F('user__date_joined'),
                is_active=F('user__is_active'),
        ).values('pk', 'username', 'email', 'name', 
                'loan_limit', 'datejoin', 'is_active')


class PatronUpdateView(
        mixins.DashboardContextMixin,
        generic.UpdateView):
    model = models.Patron
    fields = ['first_name', 'last_name']
    template_name_suffix = '_update_form'




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
        data = form.cleaned_data

        # Register User
        user = User.objects.create_user(data['username'])
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()

        # Notify system that user registered
        # Follow up Processing (e.g. create patron record)
        user_registered.send(
                sender=self.__class__,
                user=user,
                request=self.request)

        patron = user.patron

        # Save Patron Identification
        iden = data['identification']
        iden.patron = patron
        iden.save()

        patron.birth_date = data['birth_date']
        patron.address = data['address']
        patron.country = data['country']
        patron.postcode = data['postcode']
        patron.contact = data['contact']
        patron.note = data['note']
        patron.notification_type = reduce(operator.ior, data['notification_type'])
        patron.loan_duration = data['loan_duration']
        patron.renewal_limit = data['renewal_limit']
        patron.loan_limit = data['loan_limit']
        patron.save()

        return super().form_valid(form)
