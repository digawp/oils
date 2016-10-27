from rest_framework import serializers

from . import models

from oils.apps.shelving import serializers as shelving_serializers
from oils.apps.shelving import models as shelving_models
from oils.apps.account import models as account_models

class PatronLoanSerializer(serializers.ModelSerializer):

    resource = shelving_serializers.ItemSerializer(read_only=True)

    class Meta:
        model = models.Loan
        fields = ('id', 'resource', 'loan_at')
        depth = 1


class LoanRenewalSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LoanRenewal
        fields = ('loan', 'renew_at')
        read_only_fields = ('renew_at',)

    def validate(self, data):
        instance = models.LoanRenewal(**data)
        try:
            instance.clean()
        except models.ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return data

    def create(self, validated_data):
        return validated_data['loan'].renew()



class LoanReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LoanReturn
        fields = ('loan', 'return_at')
        read_only_fields = ('return_at',)


class LoanSerializer(serializers.ModelSerializer):
    
    patron = serializers.SlugRelatedField(
            slug_field='id',
            queryset=account_models.Patron.objects.all(),
            html_cutoff=100)

    item = serializers.SlugRelatedField(
            slug_field='code',
            queryset=shelving_models.Item.objects.all(),
            html_cutoff=100)

    class Meta:
        model = models.Loan
        fields = ('patron', 'item', 'loan_at')


    def validate(self, data):
        instance = models.Loan(**data)
        try:
            instance.clean()
        except models.ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return data
