from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'dashboard'
    label = 'dashboard'

    def ready(self):
        super().ready()
        self.module.autodiscover()
