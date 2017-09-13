from django.conf.urls import url
from django.conf import settings

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
    url(r'^profile/(?P<id>\d+)$', views.profile, name = "profile"),
    url(r'^like/(?P<id>\d+)$', views.like, name = 'like'),
    url(r'^likeonprofile/(?P<id>\d+)$', views.likeonprofile, name = 'likeonprofile'),
    url(r'^uploadprofile', views.simple_upload, name='uploadprofile'),
    url(r'^gethome$', views.gethome),
    url(r'^collaborate/(?P<id>\d+)$', views.collaborate, name = 'collaborations'),

]
