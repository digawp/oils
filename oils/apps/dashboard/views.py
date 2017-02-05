from django.shortcuts import render
from django.views import generic
from django.conf import settings

from . import mixins as dashboard_mixins

class DashboardIndexView(dashboard_mixins.DashboardContextMixin, generic.TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['sitenavs'] = settings.OILS['DASHBOARD']['MENU'].values()
        return ctx
