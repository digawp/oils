from django.core.urlresolvers import reverse_lazy


DASHBOARD_MENU = [
    {
        'label': 'Home', # Patron Dashboard
        'url': reverse_lazy('dashboard:index'),
        'access': 'patron',
        'icon': 'fa fa-home',
    },
    {
        'label': 'Summary', # Staff Dashboard
        'url': reverse_lazy('dashboard:index'),
        'access': 'staff',
        'icon': 'fa fa-home',
    },
    {
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
    },
    {
        'label': 'Circulation',
        'icon': 'fa fa-book',
        'access': 'circulator',
        'children': [
            {
                'label': 'Summary',
                'url': reverse_lazy('dashboard:circulation:loan:onestop'),
            },
            {
                'label': 'Loan Book',
                'url': reverse_lazy('dashboard:circulation:loan:new'),
            },
            {
                'label': 'Renew Book',
                'url': reverse_lazy('dashboard:circulation:loan:renewal'),
            },
            {
                'label': 'Return Book',
                'url': reverse_lazy('dashboard:circulation:loan:return'),
            },
        ]
    }
]
