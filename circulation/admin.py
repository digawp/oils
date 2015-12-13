from django.contrib import admin

from . import models

admin.site.register([models.Issue, models.Return])
