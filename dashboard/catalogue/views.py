from django.shortcuts import render
from django.views import generic
from django.contrib.contenttypes import models as ct_models
from django.contrib.contenttypes import generic as ct_generic
from django.core.urlresolvers import reverse
from django import http

from catalogue import models as catalogue_models

from . import forms
from . import tables

import django_tables2 as tables2


class ResourceListView(tables2.SingleTableMixin, generic.TemplateView):

    # TemplateView
    template_name = 'dashboard/catalogue/resource_list.html'

    # ResourceListView
    resourcetype_form_class = forms.ResourceTypeSelectForm

    # SingleTableMixin
    table_class = tables.ResourceTypeTable
    context_table_name = 'resource_types'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['resourcetype_form'] = self.resourcetype_form_class()
        return ctx

    def get_table_data(self):
        return [{
            'name': 'Book',                
            'slug': 'book',
        }] + list(catalogue_models.SerialType.objects.all())


class ResourceCreateUpdateView(generic.UpdateView):
    template_name = 'dashboard/catalogue/resource_update.html'

    resource_instance_formset = forms.ResourceInstanceFormSet

    def get_object(self):
        self.object = catalogue_models.ResourceInstance.objects.get(
            pk=self.kwargs['pk'])
        if 'pk' not in self.kwargs:
            return None
        else:
            return self.object.creative_work_object
            

    def get_form_class(self, **kwargs):
        if 'pk' not in self.kwargs:
            if self.kwargs['resource_type_slug'] == 'book':
                return forms.BookForm
            else:
                return forms.SerialForm
        else:
            if self.object._meta.model_name == 'book':
                return forms.BookForm
            else:
                return forms.SerialForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['resource_instance_formset'] = self.resource_instance_formset()
        return ctx

    def get_success_url(self):
        return reverse('dashboard:catalogue:resource-list')

    def form_valid(self, form):
        if 'pk' not in self.kwargs and form.is_valid():
            self.object = form.save()

        resource_instance_formset = self.resource_instance_formset(
            self.request.POST, self.request.FILES,
            instance=self.object)
        if form.is_valid() and resource_instance_formset.is_valid():
            form.save()
            resource_instance_formset.save()
        return http.HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        resource_instance_formset = self.resource_instance_formset(
            self.request.POST, self.request.FILES,
            instance=self.object)
        ctx = self.get_context_data(form=form,
                resource_instance_formset=resource_instance_formset)
        return self.render_to_response(ctx)

class ResourceCreateRedirectView(generic.RedirectView):
    permanent = False
    resourcetype_form_class = forms.ResourceTypeSelectForm

    def get_redirect_url(self, **kwargs):
        form = self.resourcetype_form_class(self.request.GET)
        if form.is_valid():
            resource_type = form.cleaned_data['resource_type']
        else:
            resource_type = 'book'
        return reverse('dashboard:catalogue:resource-create',
                kwargs={'resource_type_slug': resource_type})
