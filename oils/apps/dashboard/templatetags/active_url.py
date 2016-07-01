import re

from django import template
from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag(takes_context=True)
def active_url(context, active_url):
    try:
        pattern = '^' + reverse(active_url)
    except NoReverseMatch:
        pattern = active_url

    path = context.request.path
    if re.search(pattern, path):
        return 'active'
    return ''
