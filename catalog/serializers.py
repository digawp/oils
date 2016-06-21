from rest_framework import serializers

from . import models

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = ('title', 'agents', 'publishers',
                'subjects', 'classifications')


class Item(object):
    def __init__(self):
        self.title = title
        self.subtitle = subtitle



    
class GenericBibliographicSerializer(serializers.Serializer):
    title = serializers.CharField()
    subtitle = serializers.CharField(required=False)
    identifiers = serializers.DictField(
        child=serializers.ListField()
    )
    classifications = serializers.DictField(
        child=serializers.CharField(),
        required=False,
    )
    subjects = serializers.ListField(
        child=serializers.DictField(),
        required=False,
    )
    publishers = serializers.ListField(
        child=serializers.DictField(),
        required=False,
    )
    agents = serializers.ListField(
        child=serializers.DictField(),
        required=False,
    )


    def create(self, validated_data):
        return models.GenericBibliographic(**validated_data)


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        return instance


class BibkeyListSerializer(serializers.ListSerializer):
    def __init__(self, bibkey):
        self.bibkey = bibkey
