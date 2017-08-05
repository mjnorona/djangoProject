from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login', views.login),
    url(r'^logout$', views.logout),
    url(r'^home$', views.home),
    url(r'^edit$', views.edit),
    url(r'^edit_submit$', views.edit_submit),
    url(r'^submit/(?P<id>\d+)$', views.submit, name = "submit"),
    url(r'^solutions/(?P<id>\d+)$', views.solutions, name = "solutions"),
    url(r'^profile/(?P<id>\d+)$', views.profile),
    url(r'^like/(?P<id>\d+)$', views.like, name = 'like'),
    url(r'^logout$', views.logout)
]
