from django.contrib import admin
from django.contrib.contenttypes import admin as ct_admin
from . import models


@admin.register(models.ResourceInstance)
class ResourceInstanceAdmin(admin.ModelAdmin):
    related_lookup_fields = {
        'generic': [
            ('creative_work_type', 'creative_work_id'),
        ]
    }


class AuthorAliasInline(admin.TabularInline):
    model = models.AuthorAlias


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        AuthorAliasInline
    ]

class ResourceInstanceInlineAdmin(ct_admin.GenericTabularInline):
    model = models.ResourceInstance
    ct_field = 'creative_work_type'
    ct_fk_field = 'creative_work_id'


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [
        ResourceInstanceInlineAdmin,
    ]
    search_fields = [
        'isbn13', 'title',
    ]
    list_display = [
        'isbn13', 'title',
    ]
    prepopulated_fields = {
        'slug': [
            'isbn13'
        ]
    }

admin.site.register([models.Publisher, models.Location])
