from django.contrib import admin
from django.contrib.contenttypes import admin as ct_admin
from . import models

class BookIdentifierInline(admin.TabularInline):
    model = models.BookIdentifier
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
    raw_id_fields = ('agents','classifications')
    autocomplete_lookup_fields = {
        'm2m': ['classifications', 'agents'],
    }
    search_fields = (
            'identifiers__value', 'title', 'subtitle',
            'agents__first_name', 'agents__last_name',
            'publication__year', 'publishers__name')
    inlines = [
        BookAgentInline,
        BookIdentifierInline,
        PublisherInline
    ]

class AgentAliasInline(admin.TabularInline):
    model = models.AgentAlias

class AgentAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', )
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


admin.site.register([
    models.Series, models.BookSeries,
    models.BookIdentifier, models.BookIdentifierType,
    models.BookAgent,
    models.AgentIdentifier, models.AgentIdentifierType,
    models.Subject, models.AgentAlias,
    models.Classification, models.ClassificationType,
    models.Publication, models.Publisher,
    models.OpenLibrary,
])
