from django import template
import re

class NavItem(object):
    def __init__(self, label, url='#', icon=''):
        self.label = label
        self.url = url
        self.permission_set = set({})
        self.children = []
        self.css_class = ''
        self.icon = icon

    def css_class(self):
        return self.css_class

    def add_child(self, child):
        self.children.append(child)

    def add_permission(self, perm):
        self.permission_set.add(perm)

    def has_loan_permission(self, request):
        return request.user.has_perm('circulation:loan')

    def subnav_hide(self):
        return 'nav-hide'

    def active(self, path):
        if self.url == '' or self.url == '#':
            return
        pattern = '^' + str(self.url)
        if re.search(pattern, path):
            self.css_class += ' active'

    def html(self):
        return self.label

class DropdownNav(NavItem):
    css_class = 'dropdown-toggle'

from ... import dashboard
register = template.Library()
@register.inclusion_tag('dashboard/tabs.html', takes_context=True)
def dashboard_nav(context):
    nav_items = []
    path = context.request.path

    for nav in dashboard.DASHBOARD_NAVIGATION:
        navitem = NavItem(
            nav['label'],
            **{k: nav[k] for k in nav.keys() if k in {'url', 'icon'}}
        )
        access = nav.get('access')
        if access:
            navitem.add_permission(access)

        navitem.active(path)
        
        children = nav.get('children', [])
        if children:
            for child in children:
                ni = NavItem(
                    child['label'],
                    **{k: child[k] for k in child.keys() if k in {'url', 'icon'}}
                )
                access = nav.get('access')
                if access:
                    ni.add_permission(access)
                ni.active(path)
                navitem.add_child(ni)
        nav_items.append(navitem)

    return {
        'user': context.request.user,
        'nav_items': nav_items,
    }

