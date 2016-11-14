from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import filters

from . import models
from . import serializers
from . import filters as cat_filters

class ItemViewSet(viewsets.ModelViewSet):
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    #filter_fields = ('creative_work_object__title',)
    filter_class = cat_filters.ItemFilter
    lookup_field = 'code'

