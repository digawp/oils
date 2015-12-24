class ResourceTypeMixin(object):
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['resource_type'] = self.kwargs['resourcetype']
        return ctx
