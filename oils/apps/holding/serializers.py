from rest_framework import serializers


from . import models

class ItemSerializer(serializers.ModelSerializer):
    resource_type = serializers.CharField(
            source='creative_work_object.resource_type')
    identifiers = serializers.DictField(
            source='creative_work_object.resource_identifiers')
    title = serializers.CharField(
            source='creative_work_object.title')
    class Meta:
        model = models.Item
        fields = ('code', 'resource_type',
                'identifiers', 'title', 'resource_type')

