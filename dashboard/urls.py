from django.conf.urls import include, url

from . import views
from .catalogue import urls as catalogue_urls

urlpatterns = [
    url(r'^catalogue/', include(catalogue_urls, namespace='catalogue')),
    url(r'^$', views.index, name='index'),
]
