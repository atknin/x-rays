# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from general import models as general_models
from django.contrib import auth

# Create your views here.
def index(request):
	if request.is_ajax():
		message = {}
		login = request.POST['login']
		password = request.POST['password']
		user = auth.authenticate(username=login, password=password)
		
		if user is not None:
			message['status'] = "ok"
			auth.login(request, user)
		else:
			message['status'] = "error"
		return JsonResponse(message)
	else:
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
	