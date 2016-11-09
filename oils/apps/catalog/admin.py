from django.contrib import admin
from django.contrib.contenttypes import admin as ct_admin
from . import models

from mptt.admin import DraggableMPTTAdmin

class SubjectAdmin(DraggableMPTTAdmin):
    model = models.Subject
    search_fields = (
        'name',
        'parent__name',
    )

class BookIdentifierInline(admin.TabularInline):
    model = models.BookIdentifier
    raw_id_fields = ("identifier",)
    autocomplete_lookup_fields = {
        'fk': ['identifier'],
    }
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
    autocomplete_lookup_fields = {
        'fk': ['agent'],
    }
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

class UniversalIdentifierAdmin(admin.ModelAdmin):
    search_fields = ('value', )

class PublisherAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class ClassificationAdmin(admin.ModelAdmin):
    search_fields = ('value',)

admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Agent, AgentAdmin)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.Subject, SubjectAdmin)
admin.site.register(models.UniversalIdentifier, UniversalIdentifierAdmin)
admin.site.register(models.Publisher, PublisherAdmin)
admin.site.register(models.Classification, ClassificationAdmin)


admin.site.register([
    models.UniversalIdentifierType,
    models.BookIdentifier,
    models.BookAgent,
    models.AgentIdentifier, models.AgentIdentifierType,
    models.AgentAlias,
    models.ClassificationType,
    models.Publication,
    models.OpenLibrary,
])
