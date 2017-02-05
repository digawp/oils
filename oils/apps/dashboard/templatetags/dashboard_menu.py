from django import template
from django.conf import settings

register = template.Library()
@register.inclusion_tag('dashboard/includes/topnav.html', takes_context=True)
def render_dashboard_topnav(context):
    context['topnav_items'] = settings.OILS['DASHBOARD']['MENU'].values()
    return context


@register.inclusion_tag('dashboard/includes/sidebar.html', takes_context=True)
def render_dashboard_sidebar(context):
    request = context['request']
    app_name = request.resolver_match.app_name
    context['navitem'] = settings.OILS['DASHBOARD']['MENU'][app_name]
    return context

