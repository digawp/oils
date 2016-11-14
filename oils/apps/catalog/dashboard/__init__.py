from oils.apps import dashboard


class CatalogPanel(dashboard.Panel):
    name = 'catalog'

    def get_urls(self):
        from . import urls
        return urls.urlpatterns


dashboard.site.register(CatalogPanel)
