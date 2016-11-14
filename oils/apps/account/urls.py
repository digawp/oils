from django.conf.urls import include, url

from . import routers
from . import views

urlpatterns = [
    url('^', include('django.contrib.auth.urls'))
]

api_urlpatterns = [
    #url(r'^$', views.api_root, name='root'),
    url(r'', include(routers.router.urls)),
]
