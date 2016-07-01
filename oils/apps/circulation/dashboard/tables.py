from django.utils.translation import ugettext_lazy as _
import django_tables2 as tables


from .. import models

class LoanTable(tables.Table):
    due_date = tables.DateColumn()
    actions = tables.TemplateColumn(
        verbose_name=_('Actions'),
        template_name='circulation/dashboard/loan_row_actions.html')

    class Meta:
        model = models.Loan
        fields = ('resource', 'patron',
                'loan_at', 'total_renewal', 'last_renewal', 'due_date', 
                'actions',)
