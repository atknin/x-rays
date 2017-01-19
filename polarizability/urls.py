# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from polarizability import views

urlpatterns = [
	url(r'^$', views.polarizability),
    url(r'^compute/', views.compute),
    url(r'^add_crystal/', views.add_crystal),
    url(r'^delete/', views.delete),
 
]