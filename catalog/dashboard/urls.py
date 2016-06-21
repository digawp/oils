from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # List of CreativeWork (last 20 entry)
    # Find CreativeWork (search form)
    # Find Item (barcode input)
    # add CreativeWork (edit form + CRUD of resource instances)
    # add Item (resource instance form)
    # edit CreativeWork (edit + delete + CRUD of resource instances)
    url(r'^onestop/$', views.OneStopView.as_view(), name='onestop'),
    url(r'^onestop/(?P<bibkey>[\w]+:[\w]+)/$', 
        views.OneStopView.as_view(), name='onestop'),
    url(r'^lookup/$', views.LookupView.as_view(), name='lookup'),
    url(r'^$', views.CatalogIndexView.as_view(), name='index'),
]
