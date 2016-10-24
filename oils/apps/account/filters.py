import django_filters


from . import models

class PatronFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
            name='user__username', lookup_type='icontains')
    identifications = django_filters.CharFilter(
            name='identifications__value', lookup_type='icontains')
    class Meta:
        model = models.Patron
        fields = ['username', 'identifications']
