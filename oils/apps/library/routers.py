from rest_framework import routers

from patroncirculation import views as patron_views
from catalog import views as catalog_views
from shelving import views as shelving_views
from circulation import views as circulation_views

router = routers.DefaultRouter()
router.register(r'patrons', patron_views.PatronViewSet)
#router.register(r'users', patron_views.UserViewSet)
router.register(r'items', shelving_views.ItemViewSet)
router.register(r'books', catalog_views.BookViewSet)
router.register(r'loans', circulation_views.LoanViewSet)
router.register(r'loans-renewals', circulation_views.LoanRenewalViewSet)
router.register(r'loans-returns', circulation_views.LoanReturnViewSet)
