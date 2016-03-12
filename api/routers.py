from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'patrons', views.PatronViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'resources', views.ResourceViewSet)
router.register(r'loans', views.LoanViewSet)
router.register(r'loans-renewals', views.LoanRenewalViewSet)
router.register(r'loans-returns', views.LoanReturnViewSet)
