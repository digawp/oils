from django.views import generic

class DashboardContextMixin(generic.base.ContextMixin):

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx
