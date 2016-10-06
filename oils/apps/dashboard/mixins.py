from django.views import generic
from django.conf import settings

from . import defaults as dashboard_defaults

import re

def process_data(nav):
    data = {
        'label': nav['label'],
    }

    data['url'] = str(nav['url'])

    if 'icon' in nav:
        data['icon'] = nav['icon']

    data['children'] = [
            process_data(child) for child in nav.get('children', [])]
    return data

class DashboardContextMixin(generic.base.ContextMixin):
    def _process_dashboard_menu(self, menu_data):
        menu_items = []
        for nav in menu_data:
            req_perm = nav.get('access')
            if req_perm and not self.request.user.has_perm(req_perm):
                continue

            data = process_data(nav)

            menu_items.append(data)
        return menu_items

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        initial_data = ctx.get(
            'initial_data', { 'dashboard': {} }
        )

        initial_data['dashboard']['menu'] = self._process_dashboard_menu(
                settings.OILS['DASHBOARD']['MENU'])
        ctx['initial_data'] = initial_data
        return ctx
