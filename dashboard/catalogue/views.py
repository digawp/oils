from django.shortcuts import render
from django.views import generic

from django.core.urlresolvers import reverse

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

    def get_form_class(self, **kwargs):
        if self.kwargs['resource_type_slug'] == 'book':
            return forms.BookForm
        else:
            return forms.SerialForm


    def get_object(self, queryset=None):
        return None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx

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
