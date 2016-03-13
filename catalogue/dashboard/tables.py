from django.utils.translation import ugettext_lazy as _
import django_tables2 as tables

from catalogue import models as catalogue_models


class ResourceTypeTable(tables.Table):

    name = tables.TemplateColumn(
        verbose_name=_('Resource Type'),
        template_name='dashboard/catalogue/resourcetype_row_name.html')

    actions = tables.TemplateColumn(
        verbose_name=_('Actions'),
        template_name='dashboard/catalogue/resourcetype_row_actions.html',
        orderable=False)

    class Meta:
        fields = ('name', 'actions',)

class ResourceTable(tables.Table):

    resource_identifier = tables.LinkColumn(
            'dashboard:catalogue:resource:update', kwargs={
                'resourcetype': tables.A('resource_type'),
                'identifier' : tables.A('resource_identifier')
            }, verbose_name=_('ISBN/ISSN'))

    title = tables.TemplateColumn(
        verbose_name=_('Title'),
        template_name='dashboard/catalogue/resource_row_title.html')

    actions = tables.TemplateColumn(
        verbose_name=_('Actions'),
        template_name='dashboard/catalogue/resource_row_actions.html')

    class Meta:
        model = catalogue_models.ResourceInstance
        fields = ('resource_identifier', 'title', 'actions',)
