# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from diffraction import views

urlpatterns = [
	url(r'^0/$', views.diffraction_0),
    url(r'^compute/', views.compute), 
]