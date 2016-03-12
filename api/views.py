from django.shortcuts import render
from django.contrib.auth import models as auth_models

from rest_framework import viewsets

from patron import models as patron_models
from catalogue import models as catalogue_models
from circulation import models as circulation_models

from rest_framework import filters

from . import serializers
from . import filters as api_filters


class PatronViewSet(viewsets.ModelViewSet):
    queryset = patron_models.Patron.objects.all()
    serializer_class = serializers.PatronSerializer
    filter_class = api_filters.PatronFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = auth_models.User.objects.all()
    serializer_class = serializers.UserSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = catalogue_models.ResourceInstance.objects.all()
    serializer_class = serializers.ResourceInstanceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    #filter_fields = ('creative_work_object__title',)
    filter_class = api_filters.ResourceInstanceFilter


class LoanViewSet(viewsets.ModelViewSet):
    queryset = circulation_models.Loan.objects.all()
    serializer_class = serializers.LoanSerializer


class LoanRenewalViewSet(viewsets.ModelViewSet):
    queryset = circulation_models.LoanRenewal.objects.all()
    serializer_class = serializers.LoanRenewalSerializer


class LoanReturnViewSet(viewsets.ModelViewSet):
    queryset = circulation_models.LoanReturn.objects.all()
    serializer_class = serializers.LoanReturnSerializer
