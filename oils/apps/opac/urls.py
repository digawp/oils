from django.conf.urls import include, url

from . import views

#urlpatterns = [
#    url(r'^', include('haystack.urls')),
#]

urlpatterns = [
    url(r'^$', views.opac_view, name='search_view'),
]
