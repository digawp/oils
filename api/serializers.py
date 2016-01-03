from rest_framework import serializers

from patron import models as patron_models
from catalogue import models as catalogue_models

from django.contrib.auth import models as auth_models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = auth_models.User
        fields = ('url', 'username', 'email', 'is_staff')

class PatronSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = patron_models.Patron
        fields = ('url', 'loan_limit', 'username', 'email')
        depth = 1


class ResourceInstanceSerializer(serializers.HyperlinkedModelSerializer):
    resource_type = serializers.CharField(
            source='creative_work_object.resource_type')
    resource_identifier = serializers.CharField(
            source='creative_work_object.resource_identifier')
    title = serializers.CharField(
            source='creative_work_object.title')
    class Meta:
        model = catalogue_models.ResourceInstance
        fields = ('url', 'code', 'resource_type',
                'resource_identifier', 'title', 'resource_type')
