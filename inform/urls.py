# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from inform import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^questions/$', views.questions),
    url(r'^questions/results/$', views.questions_results),
    url(r'^manage/$', views.manage), 

]
