"""hackerlibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from oils.apps import dashboard
from oils.apps.library import urls as lib_urls
from oils.apps.circulation import urls as circ_urls
from oils.apps.catalog import urls as cat_urls
from oils.apps.account import urls as account_urls
from oils.apps.holding import urls as holding_urls

from oils.apps.library import views as library_views

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', include(dashboard.site.urls)),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^api/', include([
        url(r'^catalogs/',
            include(cat_urls.api_urlpatterns,
                    namespace='catalog')),
        url(r'^holdings/',
            include(holding_urls.api_urlpatterns,
                    namespace='holding')),
        url(r'^circulations/',
            include(circ_urls.api_urlpatterns,
                    namespace='circulation')),
        url(r'^accounts/',
            include(account_urls.api_urlpatterns,
                    namespace='account')),
        url(r'^$', library_views.api_root, name='root'),
    ], namespace='api')),
]
