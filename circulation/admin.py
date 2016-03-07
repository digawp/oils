from django.contrib import admin

from . import models

admin.site.register([models.Loan, models.LoanReturn, models.LoanRenewal])
