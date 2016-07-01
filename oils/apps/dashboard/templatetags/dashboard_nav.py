from django import template

register = template.Library()
@register.inclusion_tag('dashboard/tabs.html', takes_context=True)
def dashboard_nav(context):
    return {
        'user': context.request.user
    }
