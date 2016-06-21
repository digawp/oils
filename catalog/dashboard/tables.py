from django.utils.translation import ugettext_lazy as _
import django_tables2 as tables

from catalog import models as catalog_models


class ResourceTypeTable(tables.Table):

    name = tables.TemplateColumn(
        verbose_name=_('Resource Type'),
        template_name='dashboard/catalog/resourcetype_row_name.html')

    actions = tables.TemplateColumn(
        verbose_name=_('Actions'),
        template_name='dashboard/catalog/resourcetype_row_actions.html',
        orderable=False)

    class Meta:
        fields = ('name', 'actions',)
