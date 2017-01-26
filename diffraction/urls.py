# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from diffraction import views

urlpatterns = [
	url(r'^([0-9]{1})/$', views.diffraction_scheme),
	url(r'^$', views.diffraction),
    url(r'^compute/$', views.compute), 
]