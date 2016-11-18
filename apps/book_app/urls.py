from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'^books/add$', views.add),
    url(r'^add_review$', views.create),
    url(r'^logout$', views.logout),
    url(r'^books/(?P<id>\d+$)', views.page),
    url(r'^users/(?P<id>\d+$)', views.users),
    url(r'^delete/(?P<id>\d+$)', views.delete)
]
