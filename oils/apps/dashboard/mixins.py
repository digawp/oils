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

def test_user_access(user, perm=None):
    # Default allow user when no permission required
    if not perm:
        return True

    # Check the Permission
    if user.has_perm(perm):
        return True

    # Alternatively user belong to a group
    if user.groups.filter(name=perm).exists():
        return True

    return False

class DashboardContextMixin(generic.base.ContextMixin):
    def _process_dashboard_menu(self, menu_data):
        menu_items = []
        for nav in menu_data:
            req_perm = nav.get('access')
            if not test_user_access(self.request.user, req_perm):
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
