# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from library import views

urlpatterns = [
	url(r'^add/$', views.add),
]
