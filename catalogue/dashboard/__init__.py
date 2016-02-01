import dashboard


class CataloguePanel(dashboard.Panel):
    name = 'catalogue'

    def get_urls(self):
        from . import urls
        return urls.urlpatterns


dashboard.site.register(CataloguePanel)
