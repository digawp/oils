from django.shortcuts import render
from django.views import generic
from django.contrib.contenttypes import models as ct_models
from django.core.urlresolvers import reverse
from django import http

from .. import models

from . import forms
from . import tables
from . import mixins

import django_tables2 as tables2
import json

from ..bibkey import Bibkey
from .. import serializers

from oils.apps.dashboard import mixins as dashboard_mixins

class CatalogIndexView(dashboard_mixins.DashboardContextMixin, generic.TemplateView):
    template_name = 'catalog/dashboard/index.html'


class OneStopView(dashboard_mixins.DashboardContextMixin, generic.TemplateView):
    template_name = 'catalog/dashboard/onestop.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        initial_data = {}
        bibkey = kwargs.get('bibkey')

        if not bibkey:
            return ctx

        try:
            oils_book = models.Book.objects.retrieve(bibkey)
            generic_bib = oils_book.to_generic_bibliographic()
            initial_data['provider'] = 'oils'
        except models.Book.DoesNotExist:
            openlibrary = models.OpenLibrary.objects.retrieve(bibkey)
            if (openlibrary.raw_json):
                generic_bib = openlibrary.to_generic_bibliographic()
            else:
                generic_bib = None
            initial_data['provider'] = 'openlibrary'

        if generic_bib:

            book = serializers.GenericBibliographicSerializer(generic_bib)
            initial_data['item'] = {
                'bibliographic': book.data
            }

            # Existing OILS Record
            if initial_data['provider'] == 'oils':
                initial_data['item']['shelving'] = {}
                initial_data['item']['annotations'] = {}

            ctx['initial_data'] = json.dumps(initial_data)
        return ctx

class LookupView(dashboard_mixins.DashboardContextMixin, generic.FormView):
    template_name = 'catalog/dashboard/lookup.html'
    form_class = forms.LookupForm
