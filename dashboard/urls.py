from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views
from .catalogue import urls as catalogue_urls
from .circulation import urls as circulation_urls

urlpatterns = [
    url(r'^catalogue/', include(catalogue_urls, namespace='catalogue')),
    url(r'^circulation/', include(circulation_urls, namespace='circulation')),
    url(r'^$', login_required(views.DashboardView.as_view()), name='index'),
]
