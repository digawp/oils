from django.utils.translation import ugettext_lazy as _
import django_tables2 as tables


from circulation import models

class IssueTable(tables.Table):
    actions = tables.TemplateColumn(
        verbose_name=_('Actions'),
        template_name='dashboard/circulation/issue_row_actions.html')

    class Meta:
        model = models.Issue
        fields = ('resource', 'patron', 'loan_at', 'actions',)
