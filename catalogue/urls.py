from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<resourcetype>[\w-]+)/(?P<slug>[\w-]+)/$',
        views.ResourceDetailView.as_view(),
        name='detail'),
]
