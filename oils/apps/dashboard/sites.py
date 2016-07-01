from functools import update_wrapper

from django.conf.urls import url, include
from django.http import HttpResponse

from django.shortcuts import render

class DashboardSite(object):

    def __init__(self, name='dashboard'):
        self.name = name
        self._registry = set()

    def register(self, panel_class):
        panel_obj = panel_class()
        self._registry.add(panel_obj)

    def get_urls(self):

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.dashboard_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        urlpatterns = [
            url(r'^$', wrap(self.index), name='index'),
        ]

        for panel in self._registry:
            urlpatterns += [
                url(r'^{}/'.format(panel.name), include(panel.urls)),
            ]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'dashboard', self.name

    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff

    def dashboard_view(self, view):
        def wrapper(request, *args, **kwargs):
            if not self.has_permission(request):
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            return view(request, *args, **kwargs)

        return update_wrapper(wrapper, view)

    def index(self, request):
        return render(request, 'dashboard/index.html', {})


site = DashboardSite()
