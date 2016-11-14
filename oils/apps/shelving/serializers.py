from rest_framework import serializers


from . import models

class ItemSerializer(serializers.ModelSerializer):
    resource_type = serializers.CharField(
            source='creative_work_object.resource_type')
    identifiers = serializers.DictField(
            source='creative_work_object.resource_identifiers')
    title = serializers.CharField(
            source='creative_work_object.title')
    subtitle = serializers.CharField(
            source='creative_work_object.subtitle')
    authors = serializers.StringRelatedField(
            many=True,
            source='book.authors')
    classifications = serializers.SlugRelatedField(
            slug_field='value', many=True,
            read_only=True, source='book.classifications')
    class Meta:
        model = models.Item
        fields = ('code', 'resource_type',
                'identifiers', 'title', 'resource_type', 'authors', 'classifications',
                'subtitle', )

