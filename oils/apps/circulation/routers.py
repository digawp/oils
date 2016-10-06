from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'loans', views.LoanViewSet)
router.register(r'loans-renewal', views.LoanRenewalViewSet)
router.register(r'loans-returns', views.LoanReturnViewSet)
