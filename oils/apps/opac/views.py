from django.shortcuts import render

from haystack.generic_views import SearchView

class OPACView(SearchView):
    """OPAC search view."""

opac_view = OPACView.as_view()
