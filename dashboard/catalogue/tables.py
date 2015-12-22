from django.utils.translation import ugettext_lazy as _
import django_tables2 as tables2

from catalogue import models as catalogue_models


class ResourceTypeTable(tables2.Table):

    name = tables2.TemplateColumn(
        verbose_name=_('Resource Type'),
        template_name='dashboard/catalogue/resourcetype_row_name.html')

    actions = tables2.TemplateColumn(
        verbose_name=_('Actions'),
        template_name='dashboard/catalogue/resourcetype_row_actions.html',
        orderable=False)

    class Meta:
        model = catalogue_models.SerialType
        fields = ('name', 'actions',)

class ResourceInstanceTable(tables2.Table):
    
    class Meta:
        model = catalogue_models.ResourceInstance
