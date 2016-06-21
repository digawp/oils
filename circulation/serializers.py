from rest_framework import serializers

from . import models

from holding import serializers as holding_serializers
from holding import models as holding_models
from patron import models as patron_models

class PatronLoanSerializer(serializers.ModelSerializer):

    resource = holding_serializers.ItemSerializer(read_only=True)

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
            queryset=patron_models.Patron.objects.all())

    item = serializers.SlugRelatedField(
            slug_field='code',
            queryset=holding_models.Item.objects.all())

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
