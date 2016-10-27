from django.shortcuts import render
from django.views import generic

from rest_framework import viewsets
from rest_framework import status
from rest_framework import views as drf_views
from rest_framework import generics as drf_generics
from rest_framework import response as drf_response

from . import models
from . import serializers
from . import openlibrary
from .bibkey import Bibkey


class ResourceDetailView(generic.DetailView):
    model = models.Book
    template_name = 'catalog/resource_detail.html'


class BookViewSet(viewsets.ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    lookup_field = 'isbn'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        self.kwargs[self.lookup_field]
        isbn = self.kwargs['isbn']
        
        if len(self.kwargs['isbn']) == 13:
            self.lookup_field = 'isbn13'
        elif len(self.kwargs['isbn']) == 10:
            self.lookup_field = 'isbn10'
        else:
            raise

        filter_kwargs = {self.lookup_field: self.kwargs['isbn']}
        
        try:
            obj = queryset.get(**filter_kwargs)
        except ObjectDoesNotExist:
            wc = WorldCat()
            raw_data = wc.lookup_by_isbn(isbn)
            serialized_data = raw_data
            obj = catalog_models.Book.objects.create(**serialized_data)
            raise
        finally:
            self.check_object_permissions(self.request, obj)
            return obj
        

class OpenLibraryBibliographicView(drf_views.APIView):
    """Openlibrary provider API.

    This resource will make a http request to OpenLibrary API. However
    if openlibrary cached record exist in our database,
    it will return the cached records instead.
    
    """
    def get(self, request, identifiertype, identifiervalue, format=None):
        bibkey = Bibkey(identifiertype, identifiervalue)
        obj = models.OpenLibrary.objects.retrieve(bibkey)
        bibliographic = obj.to_generic_bibliographic()
        serializer = serializers.GenericBibliographicSerializer(bibliographic)
        if serializer:
            return drf_response.Response(serializer.data)
        else:
            return drf_response.Response(bibkey,
                    status=status.HTTP_404_NOT_FOUND)


class BibkeyView(drf_generics.ListAPIView):
    """List of all identifiers"""
    def list(self, *args, **kwargs):
        return drf_response.Response(
            models.BookIdentifierType.objects.bibkey_list())

bibkey_view = BibkeyView.as_view()
