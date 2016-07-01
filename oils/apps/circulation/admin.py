from django.contrib import admin
from django.utils import timezone
from . import models
from . import forms


class LoanRenewalInline(admin.TabularInline):
    model = models.LoanRenewal
    extra = 0

    def get_max_num(self, request, obj=None, **kwargs):
        if obj:
            return obj.loanrenewal_set.count() + 1
        else:
            return 0


@admin.register(models.Loan)
class LoanAdmin(admin.ModelAdmin):
    inlines = [
        LoanRenewalInline,
    ]
    form = forms.LoanForm
    readonly_fields = ('loan_at',)

admin.site.register([models.LoanReturn, models.LoanRenewal])
