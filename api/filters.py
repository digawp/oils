import django_filters
from catalogue import models as catalogue_models
from patron import models as patron_models

def available(qs, value):
    if value:
        return qs.available()
    else:
        return qs.unavailable()


class ResourceInstanceFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(name='code', lookup_type='icontains')

    is_available = django_filters.BooleanFilter(action=available)

    class Meta:
        model = catalogue_models.ResourceInstance
        fields = ['code', 'is_available']



class PatronFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(name='user__username', lookup_type='icontains')
    class Meta:
        model = patron_models.Patron
        fields = ['username']
