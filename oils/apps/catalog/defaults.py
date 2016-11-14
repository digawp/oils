from django.conf import settings

OILS_DASHBOARD_MENU = getattr(settings, 'OILS_DASHBOARD_MENU', [])

OILS_DASHBOARD_MENU.append({
    'label': 'Catalog',
    'icon': 'fa fa-book',
    'access': 'cataloger',
    'children': [
        {
            'label': 'New Bibliographic',
            'url': reverse_lazy('dashboard:catalog:onestop'),
        },
        {
            'label': 'Add Book',
            'url': '',
        },
        {
            'label': 'Delete Book',
            'url': '',
        }
    ]
})

