from oils.apps import dashboard


class CirculationPanel(dashboard.Panel):
    name = 'circulation'

    def get_urls(self):
        from . import urls
        return urls.urlpatterns


dashboard.site.register(CirculationPanel)
