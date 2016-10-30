from collections import OrderedDict
from django.shortcuts import render

from rest_framework import views
from rest_framework.reverse import reverse
from rest_framework.response import Response


def home(request):
    return render(request, 'library/index.html')

api_root_dict = {
    'circulations': 'circulation:api-root',
    'memberships': 'account:api-root',
    'catalogs': 'catalog:api-root',
    'shelving': 'shelving:api-root',
}

class APIRoot(views.APIView):
    def get(self, request, *args, **kwargs):

        # Return a plain {"name": "hyperlink"} response.
        ret = OrderedDict()
        namespace = request.resolver_match.namespace
        for key, url_name in api_root_dict.items():
            if namespace:
                url_name = namespace + ':' + url_name
            try:
                ret[key] = reverse(
                    url_name,
                    args=args,
                    kwargs=kwargs,
                    request=request,
                    format=kwargs.get('format', None)
                )
            except NoReverseMatch:
                continue

        return Response(ret)

api_root = APIRoot.as_view()
