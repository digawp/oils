import dashboard


class PatronPanel(dashboard.Panel):
    name = 'patron'

    def get_urls(self):
        from . import urls
        return urls.urlpatterns


dashboard.site.register(PatronPanel)
