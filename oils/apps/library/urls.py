from django.conf.urls import include, url

from . import views
#from . import routers


urlpatterns = [
#    url(r'^api/', include(routers.router.urls, namespace='api')),
    url(r'^$', views.home),
]
