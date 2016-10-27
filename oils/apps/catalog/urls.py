from django.conf.urls import include, url
from . import views
from . import routers

urlpatterns = [
    url(r'^books/(?P<pk>[\w-]+)/$',
        views.ResourceDetailView.as_view(),
        name='detail'),
]

api_urlpatterns = [
    url(r'^openlibrary/', include([
        url(r'^(?P<identifiertype>[\w-]+)/(?P<identifiervalue>[\w-]+)/$',
            views.OpenLibraryBibliographicView.as_view(),
            name='lookup'),
        ], namespace='openlibrary')),
    url(r'^bibkeys/', views.bibkey_view, name='bibkey'),
    url(r'', include(routers.router.urls)),
]
