from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # List of CreativeWork (last 20 entry)
    # Find CreativeWork (search form)
    # Find ResourceInstace (barcode input)
    # add CreativeWork (edit form + CRUD of resource instances)
    # add ResourceInstance (resource instance form)
    # edit CreativeWork (edit + delete + CRUD of resource instances)

    url(r'^resource/', include([
        url(r'^$',
            login_required(views.ResourceIndexView.as_view()),
            name='index'),
        url(r'^(?P<resourcetype>[\w-]+)/$',
            login_required(views.ResourceListView.as_view()),
            name='list'),
        url(r'^(?P<resourcetype>[\w-]+)/add/$',
            login_required(views.ResourceCreateView.as_view()),
            name='add'),
        url(r'^(?P<resourcetype>[\w-]+)/update/(?P<identifier>[\w-]+)/$',
            login_required(views.ResourceUpdateView.as_view()),
            name='update'),
        url(r'^(?P<resourcetype>[\w-]+)/delete/(?P<pk>\d+)/$',
            login_required(views.ResourceDeleteView.as_view()),
            name='delete'),
    ], namespace='resource')),
    url(r'^$',
        login_required(views.ResourceIndexRedirectView.as_view()),
        name='index'),
]
