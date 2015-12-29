from rest_framework import serializers

from patron import models as patron_models

from django.contrib.auth import models as auth_models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = auth_models.User
        fields = ('url', 'username', 'email', 'is_staff')

class PatronSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = patron_models.Patron
        fields = ('url', 'user', 'loan_limit')
        depth = 1
