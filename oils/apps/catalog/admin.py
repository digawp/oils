from django.contrib import admin
from django.contrib.contenttypes import admin as ct_admin
from . import models

from mptt.admin import DraggableMPTTAdmin

class SubjectAdmin(DraggableMPTTAdmin):
    model = models.Subject

class BookIdentifierInline(admin.TabularInline):
    model = models.BookIdentifier
    raw_id_fields = ("identifier",)
    extra = 2

class PublisherInline(admin.TabularInline):
    model = models.Publisher.book_set.through
    raw_id_fields = ('publisher',)
    autocomplete_lookup_fields = {
        'fk': ['publisher'],
    }
    extra = 1


class BookAgentInline(admin.TabularInline):
    model = models.BookAgent
    extra = 1
    raw_id_fields = ('agent',)


class BookAdmin(admin.ModelAdmin):
    raw_id_fields = ('agents','classifications', 'subjects')
    autocomplete_lookup_fields = {
        'm2m': ['classifications', 'agents', 'subjects',],
    }
    search_fields = (
            'identifiers__value', 'title', 'subtitle',
            'agents__name', 'agents__name',
            'publication__year', 'publishers__name')
    inlines = [
        BookAgentInline,
        BookIdentifierInline,
        PublisherInline
    ]

class AgentAliasInline(admin.TabularInline):
    model = models.AgentAlias

class AgentAdmin(admin.ModelAdmin):
    search_fields = ('name', 'birth', 'death', )
    inlines = [
        AgentAliasInline
    ]

class RoleAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("label",)
    }


admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Agent, AgentAdmin)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.Subject, SubjectAdmin)


admin.site.register([
    models.UniversalIdentifier, models.UniversalIdentifierType,
    models.BookIdentifier,
    models.BookAgent,
    models.AgentIdentifier, models.AgentIdentifierType,
    models.AgentAlias,
    models.Classification, models.ClassificationType,
    models.Publication, models.Publisher,
    models.OpenLibrary,
])
