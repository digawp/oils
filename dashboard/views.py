from django.shortcuts import render
from django.views import generic

from braces import views as braces_views


class BaseDashboardView(braces_views.LoginRequiredMixin, generic.TemplateView):
    pass

class DashboardView(BaseDashboardView):
    template_name = 'dashboard/index.html'
    
