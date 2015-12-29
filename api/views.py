from django.shortcuts import render
from django.contrib.auth import models as auth_models

from rest_framework import viewsets

from patron import models as patron_models

from . import serializers


class PatronViewSet(viewsets.ModelViewSet):
    queryset = patron_models.Patron.objects.all()
    serializer_class = serializers.PatronSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = auth_models.User.objects.all()
    serializer_class = serializers.UserSerializer
