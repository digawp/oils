from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views
from .catalogue import urls as catalogue_urls

urlpatterns = [
    url(r'^catalogue/', include(catalogue_urls, namespace='catalogue')),
    url(r'^$', login_required(views.DashboardView.as_view()), name='index'),
]
