from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [

    url(r'^loans/', include([
        # List of all opened loans (not returned) (patron, admin)
        # List of all loans (patron, admin)
        # List of all closed loans (returned) (patron, admin)

        url(r'^index/$',
            login_required(views.LoanIndexView.as_view()),
            name='index'),

        # Renew (patron, admin)
        url(r'^renewal/$',
            login_required(views.LoanRenewalView.as_view()),
            name='renewal'),

        # Return loan (admin)
        url(r'^return/$',
            login_required(views.LoanReturnView.as_view()),
            name='return'),

        # New loan (admin)
        url(r'^new/$',
            login_required(views.LoanCreateView.as_view()),
            name='new'),

        # Success loan (admin)
        url(r'^success/$',
            login_required(views.LoanSuccessView.as_view()),
            name='success'),

    ], namespace='loan')),
    url(r'^$',
        login_required(views.CirculationIndexRedirectView.as_view()),
        name='index'),
]
