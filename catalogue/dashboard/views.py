from django.shortcuts import render
from django.views import generic
from django.contrib.contenttypes import models as ct_models
from django.contrib.contenttypes import generic as ct_generic
from django.core.urlresolvers import reverse
from django import http

from catalogue import models as catalogue_models

from . import forms
from . import tables
from . import mixins

import django_tables2 as tables2


class ResourceIndexRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse('dashboard:catalogue:resource:index')

class ResourceIndexView(tables2.SingleTableMixin, generic.TemplateView):
    """
    Displaying Resource Types, such as:
    - book
    - newspaper
    """
    template_name = 'dashboard/catalogue/index.html'
    table_class = tables.ResourceTypeTable
    context_table_name = 'resource_types'

    def get_table_data(self):
        return [{
            'name': 'Book',                
            'slug': 'book',
        }] + list(catalogue_models.SerialType.objects.all())

class ResourceListView(
        tables2.SingleTableMixin,
        mixins.ResourceTypeMixin, 
        generic.ListView):
    """List view for a particular type. e.g.
    - book list
    - newspaper list
    - movie list
    """

    template_name = 'dashboard/catalogue/resource_list.html'

    # SingleTableMixin
    table_class = tables.ResourceTable
    context_table_name = 'resources'
    table_pagination = {
        'per_page': 10,
    }

    def get_queryset(self):
        res_type = self.kwargs['resourcetype']
        if res_type == 'book':
            qs = catalogue_models.Book.objects.all()
        else:
            qs = catalogue_models.Serial.objects.filter(serial_type=res_type)
        return qs
            


class ResourceCreateView(
        mixins.ResourceTypeMixin,        
        generic.CreateView):
    """Creation of resource bibliographic record, e.g.
    - Add Book biblio record
    - Add Newspaper biblio record
    """

    formset_class = forms.ResourceInstanceFormSet
    template_name = 'dashboard/catalogue/resource_add.html'

    def get_success_url(self):
        return reverse('dashboard:catalogue:resource:list', kwargs={
            'resourcetype': self.object.resource_type
        })


    def get_form_class(self, **kwargs):
        if self.kwargs['resourcetype'] == 'book':
            return forms.BookForm
        else:
            return forms.SerialForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['formset'] = self.formset_class()
        return ctx

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()

        formset = self.formset_class(
            self.request.POST, self.request.FILES,
            instance=self.object)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
        return http.HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        formset = self.formset_class(
            self.request.POST, self.request.FILES,
            instance=self.object)
        ctx = self.get_context_data(form=form,
                formset=formset)
        return self.render_to_response(ctx)

class ResourceUpdateView(
        mixins.ResourceTypeMixin,        
        generic.UpdateView):
    """Editing of resource bibliographic record, e.g.
    - Edit Book biblio record
    - Edit Newspaper biblio record
    """

    formset_class = forms.ResourceInstanceFormSet
    template_name = 'dashboard/catalogue/resource_add.html'

    def get_object(self):
        if self.kwargs['resourcetype'] == 'book':
            return catalogue_models.Book.objects.get(
                    isbn13=self.kwargs['identifier'])
        else:
            return catalogue_models.Serial.objects.get(
                    serial_type__slug=self.kwargs['resourcetype'],
                    issn=self.kwargs['identifier'])

    def get_success_url(self):
        return reverse('dashboard:catalogue:resource:list', kwargs={
            'resourcetype': self.object.resource_type
        })

    def get_form_class(self, **kwargs):
        if self.kwargs['resourcetype'] == 'book':
            return forms.BookForm
        else:
            return forms.SerialForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['formset'] = self.formset_class(instance=self.object)
        return ctx

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()

        formset = self.formset_class(
            self.request.POST, self.request.FILES,
            instance=self.object)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
        return http.HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        formset = self.formset_class(
            self.request.POST, self.request.FILES,
            instance=self.object)
        ctx = self.get_context_data(form=form,
                formset=formset)
        return self.render_to_response(ctx)

class ResourceDeleteView(
        mixins.ResourceTypeMixin,        
        generic.DeleteView):
    """Deletion of resource bibliographic record, e.g.
    - Delete Book biblio record
    - Delete Newspaper biblio record
    """

    model = catalogue_models.ResourceInstance
    template_name = 'dashboard/catalogue/resource_delete.html'
    
    def get_success_url(self):
        return reverse('dashboard:catalogue:resource:list', kwargs={
            'resourcetype': self.object.resource_type
        })

