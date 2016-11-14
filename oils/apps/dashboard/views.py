from django.shortcuts import render
from django.views import generic

from . import mixins as dashboard_mixins

class DashboardIndexView(dashboard_mixins.DashboardContextMixin, generic.TemplateView):
    template_name = 'dashboard/index.html'
    
