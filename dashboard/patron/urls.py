from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [

    url(r'^$',
        login_required(views.PatronIndexView.as_view()),
        name='index'),
]
