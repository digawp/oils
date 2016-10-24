from rest_framework import serializers
from patron import serializers as patron_serializers
from patron import models as account_models
from circulation import models as circulation_models
from holding import serializers as holding_serializers


class PatronLoanSerializer(serializers.ModelSerializer):
    resource = holding_serializers.ItemSerializer(read_only=True)

    class Meta:
        model = circulation_models.Loan
        fields = ('id', 'resource', 'loan_at')
        depth = 1


class PatronSerializer(serializers.ModelSerializer):
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
        model = account_models.Patron
        fields = (
            'id', 'loan_limit', 'username', 'email', 'loans',
            'first_name', 'last_name', 'name',)


    def get_loans(self, patron):
        loans = circulation_models.Loan.opens.filter(patron=patron)
        serializer = PatronLoanSerializer(instance=loans, many=True,
                                          context=self.context)
        return serializer.data


