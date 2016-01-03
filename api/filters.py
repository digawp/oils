import django_filters
from catalogue import models as catalogue_models
from patron import models as patron_models


class ResourceInstanceFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(name='code', lookup_type='icontains')
    class Meta:
        model = catalogue_models.ResourceInstance
        fields = ['code']


class PatronFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(name='user__username', lookup_type='icontains')
    class Meta:
        model = patron_models.Patron
        fields = ['username']
