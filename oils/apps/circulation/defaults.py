
from django.conf import settings


OILS_DASHBOARD_MENU = [
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
