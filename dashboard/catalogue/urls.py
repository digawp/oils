from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^resource/create/$',
        views.ResourceCreateRedirectView.as_view(),
        name='resource-create'),
    url(r'^resource/create/(?P<resource_type_slug>[\w-]+)/$',
        views.ResourceCreateUpdateView.as_view(),
        name='resource-create'),
    url(r'^$', views.ResourceListView.as_view(), name='resource-list'),
]
