from rest_framework import serializers

from django.contrib.auth import get_user_model
User = get_user_model()


from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class PatronIdentificationSerializer(serializers.ModelSerializer):
    id_type = serializers.StringRelatedField()
    class Meta:
        model = models.PatronIdentification
        fields = ('id_type', 'value')


class PatronSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(
            source='user.first_name', write_only=True)
    last_name = serializers.CharField(
            source='user.last_name', write_only=True)
    name = serializers.CharField(
            source='user.get_full_name', read_only=True)

    identifications = PatronIdentificationSerializer(many=True)


    class Meta:
        model = models.Patron
        fields = (
            'loan_limit', 'username', 'email', 'identifications',
            'first_name', 'last_name', 'name', 'birth_date',
            'address', 'country', 'postcode', 'contact',
            'note', 'notification_type',
            'loan_duration', 'loan_limit', 'renewal_limit')

class MembershipTypeSerializer(serializers.ModelSerializer):
    loan_duration = serializers.IntegerField(source='borrowingprivillage.loan_duration')
    loan_limit = serializers.IntegerField(source='borrowingprivillage.loan_limit')
    renewal_limit = serializers.IntegerField(source='borrowingprivillage.renewal_limit')
    class Meta:
        model = models.MembershipType
        fields = ('id', 'name', 'description', 'loan_duration', 'renewal_limit', 'loan_limit')

