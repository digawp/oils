import django_tables2 as tables


from circulation import models

class IssueTable(tables.Table):
    class Meta:
        model = models.Issue
        fields = ('resource', 'patron', 'loan_at')
