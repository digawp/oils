from django.contrib import admin
from django.utils import timezone
from . import models
from . import forms

class BorrowingPrivillageInline(admin.TabularInline):
    model = models.BorrowingPrivillage
    extra = 1

from oils.apps.account import models as account_models
from oils.apps.account import admin as account_admin
account_admin.MembershipTypeAdmin.inlines += [BorrowingPrivillageInline]
admin.site.unregister(account_models.MembershipType)
admin.site.register(account_models.MembershipType,
        account_admin.MembershipTypeAdmin)


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
    raw_id_fields = ("item", "patron",)

admin.site.register([models.LoanReturn, models.LoanRenewal])
