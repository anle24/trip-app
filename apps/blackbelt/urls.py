from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^travels$', views.dashboard),
    url(r'^process_logreg$', views.process_logreg),
    url(r'^logout$', views.logout),
    url(r'^travels/add$', views.addpage),
    url(r'^addtrip$', views.addtrip),
    url(r'^travels/destination/(?P<id>\d+)$', views.destination),
    url(r'^travels/destination/join/(?P<id>\d+)$', views.join)
]
