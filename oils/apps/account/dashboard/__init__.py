from oils.apps import dashboard


class AccountPanel(dashboard.Panel):
    name = 'account'

    def get_urls(self):
        from . import urls
        return urls.urlpatterns


dashboard.site.register(AccountPanel)
