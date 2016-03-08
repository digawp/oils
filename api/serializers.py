from rest_framework import serializers

from patron import models as patron_models
from catalogue import models as catalogue_models
from circulation import models as circulation_models

from django.contrib.auth import models as auth_models


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



class PatronLoanSerializer(serializers.HyperlinkedModelSerializer):

    resource = ResourceInstanceSerializer(read_only=True)

    class Meta:
        model = circulation_models.Loan
        fields = ('url', 'resource', 'loan_at')
        depth = 1


class LoanRenewalSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = circulation_models.LoanRenewal
        fields = ('url', 'loan', 'renew_at')

    def validate(self, data):
        instance = circulation_models.LoanRenewal(**data)
        try:
            instance.clean()
        except circulation_models.ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return data


class LoanReturnSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = circulation_models.LoanReturn
        fields = ('url', 'loan', 'return_at')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = auth_models.User
        fields = ('url', 'username', 'email', 'is_staff')

class PatronSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(
            source='user.first_name', write_only=True)
    last_name = serializers.CharField(
            source='user.last_name', write_only=True)
    name = serializers.CharField(
            source='user.get_full_name', read_only=True)

    loans = serializers.SerializerMethodField()

    

    class Meta:
        model = patron_models.Patron
        fields = (
            'url', 'id', 'loan_limit', 'username', 'email',
            'first_name', 'last_name', 'name', 'loans')


    def get_loans(self, patron):
        loans = circulation_models.Loan.opens.filter(patron=patron)
        serializer = PatronLoanSerializer(instance=loans, many=True,
                context=self.context)
        return serializer.data


class LoanSerializer(serializers.HyperlinkedModelSerializer):
    
    patron = serializers.SlugRelatedField(
            slug_field='id',
            queryset=patron_models.Patron.objects.all())

    resource = serializers.SlugRelatedField(
            slug_field='code',
            queryset=catalogue_models.ResourceInstance.objects.all())

    class Meta:
        model = circulation_models.Loan
        fields = ('url', 'patron', 'resource', 'loan_at')


    def validate(self, data):
        instance = circulation_models.Loan(**data)
        try:
            instance.clean()
        except circulation_models.ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return data
