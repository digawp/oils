import django_filters

from . import models

def available(qs, value):
    if value:
        return qs.available()
    else:
        return qs.unavailable()


class ItemFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(name='code', lookup_type='icontains')

    is_available = django_filters.BooleanFilter(action=available)

    class Meta:
        model = models.Item
        fields = ['code', 'is_available']


