from .sites import site
from .panels import Panel

from django.utils.module_loading import autodiscover_modules


__all__ = [
    'site', 'Panel', 'autodiscover',
]

def autodiscover():
    autodiscover_modules('dashboard', register_to=site)



default_app_config = 'dashboard.apps.DashboardConfig'


