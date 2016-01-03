from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [

    url(r'^issues/', include([
        # List of all opened issues (not returned) (patron, admin)
        # List of all issues (patron, admin)
        # List of all closed issues (returned) (patron, admin)
        url(r'^$',
            login_required(views.IssueIndexView.as_view()),
            name='index'),

        # Renew (patron, admin)
        url(r'^(?P<pk>\d+)/renewal/$',
            login_required(views.IssueRenewalView.as_view()),
            name='renewal'),

        # Return issue (admin)
        url(r'^(?P<pk>\d+)/return/$',
            login_required(views.IssueReturnView.as_view()),
            name='return'),

        # Delete (admin)
        url(r'^(?P<pk>\d+)/delete/$',
            login_required(views.IssueDeleteView.as_view()),
            name='delete'),

        # New issue (admin)
        url(r'^new/$',
            login_required(views.IssueCreateView.as_view()),
            name='new'),

    ], namespace='issue')),
    url(r'^$',
        login_required(views.CirculationIndexRedirectView.as_view()),
        name='index'),
]
