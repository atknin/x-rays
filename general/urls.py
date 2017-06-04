# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from general import views

urlpatterns = [
    url(r'^$', views.index),
	url(r'^about/$', views.about),
	url(r'^updates/$', views.updates),
	url(r'^converter/$', views.converter),
]
