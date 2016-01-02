import django_filters
from catalogue import models as catalogue_models


class ResourceInstanceFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(name='code', lookup_type='icontains')
    class Meta:
        model = catalogue_models.ResourceInstance
        fields = ['code']


