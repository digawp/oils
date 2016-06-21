from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views
from .catalog import urls as catalog_urls
from .circulation import urls as circulation_urls
from .patron import urls as patron_urls

urlpatterns = [
    url(r'^catalog/', include(catalog_urls, namespace='catalog')),
    url(r'^circulation/', include(circulation_urls, namespace='circulation')),
    url(r'^patron/', include(patron_urls, namespace='patron')),
    url(r'^$', login_required(views.DashboardView.as_view()), name='index'),
]
