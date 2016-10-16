import django_tables2 as tables

from django.utils.translation import ugettext_lazy as _

from .. import models

class PatronTable(tables.Table):
    username = tables.Column(verbose_name=_('Username'))
    email = tables.EmailColumn(verbose_name=_('Email'))
    name = tables.Column(verbose_name=_('Full name'))
    datejoin = tables.Column(verbose_name=_('Date joined'))
    actions = tables.TemplateColumn(
        verbose_name=_('Actions'),
        template_name='patron/dashboard/patron_row_actions.html',
        orderable=False)

    class Meta:
        model = models.Patron
        fields = (
            'username', 'name', 'email', 'loan_limit',
            'datejoin', 'actions')
