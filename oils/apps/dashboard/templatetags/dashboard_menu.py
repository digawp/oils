from django import template
from django.conf import settings

register = template.Library()
@register.inclusion_tag('dashboard/includes/topnav.html', takes_context=True)
def render_dashboard_topnav(context):
    context['topnav_items'] = settings.OILS['DASHBOARD']['MENU']
    return context
