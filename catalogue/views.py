from django.shortcuts import render
from django.views import generic

from . import models


class ResourceDetailView(generic.DetailView):

    template_name = 'catalogue/resource_detail.html'

    def get_object(self):
        return models.Book.objects.get(
                slug=self.kwargs['slug'])
