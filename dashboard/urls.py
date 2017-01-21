# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from dashboard import views

urlpatterns = [
	url(r'^$', views.dashboard),
    # url(r'^compute/', views.compute),
 
]