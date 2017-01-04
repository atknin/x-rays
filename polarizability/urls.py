# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from polarizability import views

urlpatterns = [
	url(r'^$', views.polarizability),
    url(r'^compute/', views.compute),
]