from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import viewsets

from . import models
from . import serializers
from . import filters

# Create your views here.

class PatronViewSet(viewsets.ModelViewSet):
    queryset = models.Patron.objects.all()
    serializer_class = serializers.PatronSerializer
    filter_class = filters.PatronFilter
    lookup_field = 'user__username'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'user__username'

class MembershipTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.MembershipType.objects.all()
    serializer_class = serializers.MembershipTypeSerializer
