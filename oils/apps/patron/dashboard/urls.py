from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [

    url(r'^(?P<pk>\d+)/', include([
        url(r'^activate/$',
            login_required(views.PatronActivationView.as_view()),
            {'activate': True},
            name='activate'),
        url(r'^deactivate/$',
            login_required(views.PatronActivationView.as_view()),
            {'activate': False},
            name='deactivate'),
    ])),
    url(r'^registration/$',
        login_required(views.PatronRegistrationView.as_view()),
        name='registration'),
    url(r'^$',
        login_required(views.PatronIndexView.as_view()),
        name='index'),
]
