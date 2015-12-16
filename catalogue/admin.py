from django.contrib import admin
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

admin.site.register([models.SerialType, models.Serial,
    models.Book, models.Publisher])
