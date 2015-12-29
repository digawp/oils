from django.shortcuts import render
from django.views import generic

from . import models


class ResourceDetailView(generic.DetailView):

    template_name = 'catalogue/resource_detail.html'

    def get_object(self):
        if self.kwargs['resourcetype'] == 'book':
            return models.Book.objects.get(
                    slug=self.kwargs['slug'])
        else:
            return models.Serial.objects.get(
                    serial_type__slug=self.kwargs['resourcetype'],
                    slug=self.kwargs['slug'])
