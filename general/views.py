# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from general import models as general_models


# Create your views here.
def index(request):
 	return render(
	 	request, 'general/index.html',
	 	)

def about(request):
 	return render(
	 	request, 'general/about.html',
	 	)

def updates(request):
	args = {}
	args['update_list'] = general_models.updates.objects.all()

	return render(
		request, 'general/updates.html', args
		)
	