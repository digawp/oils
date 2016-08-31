from django.contrib import admin

from . import models

class PatronIdentificationInline(admin.TabularInline):
    model = models.PatronIdentification


class PatronAdmin(admin.ModelAdmin):
    model = models.Patron
    inlines = [
        PatronIdentificationInline
    ]


admin.site.register([
    models.Membership, models.MembershipType,
    models.IdentificationType, models.PatronIdentification])

admin.site.register(models.Patron, PatronAdmin)
