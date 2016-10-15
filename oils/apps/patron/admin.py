from django.contrib import admin

from . import models

class PatronIdentificationInline(admin.TabularInline):
    model = models.PatronIdentification


class PatronAdmin(admin.ModelAdmin):
    model = models.Patron
    inlines = [
        PatronIdentificationInline
    ]

class MembershipTypeAdmin(admin.ModelAdmin):
    model = models.MembershipType


admin.site.register([
    models.Membership,
    models.IdentificationType, models.PatronIdentification])

admin.site.register(models.Patron, PatronAdmin)
admin.site.register(models.MembershipType, MembershipTypeAdmin)
