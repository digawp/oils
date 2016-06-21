"""oils URL Configuration

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
import dashboard

from catalog import urls as catalog_urls


urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^catalog/', include('catalog.urls', namespace='catalog')),
    url(r'^search/', include('opac.urls', namespace='opac')),
    url(r'^dashboard/', include(dashboard.site.urls)),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^api/catalog/', include(catalog_urls.api_urlpatterns, namespace='api')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'', include('library.urls')),
]
