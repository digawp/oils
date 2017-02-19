import django_tables2 as tables
from django_tables2.utils import A

from django.utils.translation import ugettext_lazy as _

from .. import models

class PatronTable(tables.Table):
    username = tables.LinkColumn('dashboard:account:update', kwargs={'pk': A('pk')}, verbose_name=_('Username'))
    email = tables.EmailColumn(verbose_name=_('Email'))
    name = tables.Column(verbose_name=_('Full name'))
    datejoin = tables.Column(verbose_name=_('Date joined'))
    actions = tables.TemplateColumn(
        verbose_name=_('Actions'),
        template_name='account/dashboard/patron_row_actions.html',
        orderable=False)

    class Meta:
        model = models.Patron
        fields = (
            'username', 'name', 'email', 'loan_limit',
            'datejoin', 'actions')
        order_by = '-datejoin'
        template = 'django_tables2/bootstrap.html'
