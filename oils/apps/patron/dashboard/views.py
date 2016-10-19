from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models.functions import Concat
from django.db.models import Value as V
from django.utils.safestring import mark_safe
from django.contrib import messages
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

class PatronCreateView(
        mixins.DashboardContextMixin,
        generic.CreateView):
    """Patron Registration made by the Staff"""
    model = models.Patron
    form_class = forms.PatronCreateForm
    template_name = 'patron/dashboard/patron_registration.html'
    success_message = """
    Patron "{name}" successfully registered. 
    Follow up to <a href="{link}">Change Detail</a>.
    """

    def form_valid(self, user_form, patron_form, patron_identification_form):
        user = user_form.save()
        patron = patron_form.save(commit=False)
        patron.user = user
        patron.save()

        patron_identification_form.instance = patron
        identifications = patron_identification_form.save(commit=False)
        for identification in identifications:
            identification.patron = patron
            identification.save()


        # Notify system that user registered
        user_registered.send(
                sender=self.__class__,
                user=user,
                request=self.request)

        messages.success(self.request, self.get_success_message(patron))

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, user_form, patron_form, patron_identification_form):
        return self.render_to_response(self.get_context_data(
            user_form=user_form,
            patron_form=patron_form,
            patron_identification_form=patron_identification_form))


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if 'user_form' not in data:
            kw = self.get_form_kwargs()
            user_form_kw = kw.copy()
            data['user_form'] = forms.UserForm(**user_form_kw)

        if 'patron_identity_formset' not in data:
            kw = self.get_form_kwargs()
            iden_form_kw = kw.copy()
            data['patron_identification_formset'] = forms.PatronIdentificationFormSet(**iden_form_kw)
        return data

    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:patron:index')

    def get_success_message(self, patron):
        return mark_safe(self.success_message.format(**{
            'name': patron.user.get_full_name(),
            'link': reverse('dashboard:patron:update', args=(patron.pk,)),
        }))


    def post(self, request, *args, **kwargs):
        self.object = None

        user_form = forms.UserForm(
                data=request.POST)
        patron_form = self.form_class(
                data=request.POST)
        patron_identification_form = forms.PatronIdentificationFormSet(
                data=request.POST)
        if user_form.is_valid() and patron_form.is_valid() and patron_identification_form.is_valid():
            return self.form_valid(
                    user_form,
                    patron_form,
                    patron_identification_form)
        else:
            return self.form_invalid(
                    user_form,
                    patron_form,
                    patron_identification_form)


class PatronUpdateView(
        mixins.DashboardContextMixin,
        generic.UpdateView):

    model = models.Patron
    form_class = forms.PatronUpdateForm
    template_name = 'patron/dashboard/patron_update_form.html'

    def form_valid(self, user_form, patron_form, patron_identification_form):
        user = user_form.save()
        patron = patron_form.save(commit=False)
        patron.user = user
        patron.save()

        patron_identification_form.instance = patron
        identifications = patron_identification_form.save(commit=False)
        for identification in identifications:
            identification.patron = patron
            identification.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, user_form, patron_form, patron_identification_form):
        return self.render_to_response(self.get_context_data(
            user_form=user_form,
            patron_form=patron_form,
            patron_identification_form=patron_identification_form))

    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:patron:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if 'user_form' not in data:
            kw = self.get_form_kwargs()
            user_form_kw = kw.copy()
            user_form_kw['instance'] = kw['instance'].user
            data['user_form'] = forms.UserForm(**user_form_kw)

        if 'patron_identity_formset' not in data:
            kw = self.get_form_kwargs()
            iden_form_kw = kw.copy()
            data['patron_identification_formset'] = forms.PatronIdentificationFormSet(**iden_form_kw)
        return data

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = forms.UserForm(
                data=request.POST,
                instance=self.object.user)
        patron_form = self.form_class(
                data=request.POST,
                instance=self.object)
        patron_identification_form = forms.PatronIdentificationFormSet(
                data=request.POST,
                instance=self.object,
                queryset=self.object.identifications)
        if user_form.is_valid() and patron_form.is_valid() and patron_identification_form.is_valid():
            return self.form_valid(
                    user_form,
                    patron_form,
                    patron_identification_form)
        else:
            return self.form_invalid(
                    user_form,
                    patron_form,
                    patron_identification_form)




