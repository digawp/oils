from django.contrib import admin
from django.contrib.contenttypes import admin as ct_admin

from . import models

from catalog import models as catalog_models
from catalog.admin import BookAdmin

class BookAnnotationInline(admin.StackedInline):
    model = models.BookAnnotation

    # Grappelli class modifier (default UI does not collapse)
    classes = ('collapse open',)
    inline_classes = ('collapse open',)

BookAdmin.inlines.append(BookAnnotationInline)
admin.site.unregister(catalog_models.Book)
admin.site.register(catalog_models.Book, BookAdmin)
admin.site.register([
    models.BookAnnotation,
])
