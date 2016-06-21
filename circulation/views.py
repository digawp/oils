from django.shortcuts import render

from rest_framework import viewsets

from . import models
from . import serializers

# Create your views here.

class LoanViewSet(viewsets.ModelViewSet):
    queryset = models.Loan.objects.all()
    serializer_class = serializers.LoanSerializer


class LoanRenewalViewSet(viewsets.ModelViewSet):
    queryset = models.LoanRenewal.objects.all()
    serializer_class = serializers.LoanRenewalSerializer


class LoanReturnViewSet(viewsets.ModelViewSet):
    queryset = models.LoanReturn.objects.all()
    serializer_class = serializers.LoanReturnSerializer
