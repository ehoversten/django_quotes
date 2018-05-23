from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^dashboard/add$', views.create_quote),
    url(r'^join/(?P<quote_id>\d+)$', views.join),
    url(r'^take_off/(?P<quote_id>\d+)$', views.take_off),

    url(r'^users/(?P<user_id>\d+)$', views.show),
    url(r'^logout$', views.logout),

]
