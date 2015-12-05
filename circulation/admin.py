from django.contrib import admin

from . import models

class LendAdmin(admin.ModelAdmin):
    related_lookup_fields = {
        'generic': [
            ('resource_type', 'resource_id'),
        ]
    }

admin.site.register(models.Lend, LendAdmin)
admin.site.register([models.Return])
