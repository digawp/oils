from django.shortcuts import render
from rest_framework import viewsets
from . import serializers

from patron import models as patron_models
from patron import filters as patron_filters
from circulation import models as circulation_models

class PatronViewSet(viewsets.ModelViewSet):
    queryset = patron_models.Patron.objects.all()
    serializer_class = serializers.PatronSerializer
    filter_class = patron_filters.PatronFilter

