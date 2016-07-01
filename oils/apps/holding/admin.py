from django.contrib import admin
from django.contrib.contenttypes import admin as ct_admin

from . import models

from oils.apps.catalog import models as catalog_models
from oils.apps.catalog.admin import BookAdmin

class ItemInline(ct_admin.GenericTabularInline):
    model = models.Item
    extra = 1
    ct_field = 'creative_work_type'
    ct_fk_field = 'creative_work_id'

BookAdmin.inlines.append(ItemInline)
admin.site.unregister(catalog_models.Book)
admin.site.register(catalog_models.Book, BookAdmin)
admin.site.register([
    models.Item, models.Location
])
