# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from general import models as general_models
from django.contrib import auth
from django.http import JsonResponse

# Create your views here. dsds



def index(request):
		
	if request.is_ajax():
		message = {}
		if 'logout' in request.POST: 
			auth.logout(request)
			message['status'] = "logouted"
			return JsonResponse(message)
		
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

def converter(request):
	if request.is_ajax():
		message = {}
		message['status'] = 'ok'
		input_data = {}
		for key in request.POST:
			scan = request.POST[key].split('//')
			input_data[key] = scan
			

		return JsonResponse(input_data)
	else:
	 	return render(
		 	request, 'general/converter.html',
		 	)	