# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from inform import views

urlpatterns = [
    url(r'^$', views.index),
]
