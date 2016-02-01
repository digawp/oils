import django_tables2 as tables

from django.utils.translation import ugettext_lazy as _

from patron import models

class PatronTable(tables.Table):
    username = tables.Column(verbose_name=_('Username'))
    email = tables.EmailColumn(verbose_name=_('Email'))
    firstname = tables.Column(verbose_name=_('First name'))
    lastname = tables.Column(verbose_name=_('Last name'))
    actions = tables.TemplateColumn(
        verbose_name=_('Actions'),
        template_name='dashboard/patron/patron_row_actions.html',
        orderable=False)

    class Meta:
        model = models.Patron
        fields = (
            'username', 'firstname', 'lastname', 'email', 'loan_limit',
            'actions')
