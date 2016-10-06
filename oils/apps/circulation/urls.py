from django.conf.urls import include, url

from . import routers

api_urlpatterns = [
    url(r'', include(routers.router.urls)),
]
