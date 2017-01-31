# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from general import models as general_models
from django.contrib import auth
from django.http import JsonResponse
import random
import general.bot_inform as bot_inform

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
		valid_letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
		data = {}
		name = ''.join((random.choice(valid_letters) for i in range(5)))
		detector = int(request.POST['detector'])
		# bot_inform.sent_to_atknin_bot( str( detector ), 'v')
		with open('/home/atknin/env/xrays/media/converter/'+ name +'.dat', 'w') as out:
			out.write('%14.8s' % 'keys')
			j = 0
			for key in request.POST:
				input_q = request.POST[key].split('//')
				if len(input_q)==3:
					# bot_inform.sent_to_atknin_bot( str( str(input_q[0]).split(',')), 'v')
					data['x' + str(j)] = str(input_q[0]).split(',')
					data['y' + str(j)] = str(input_q[detector]).split(',')
					j+=1
					out.write('%14.8s' % key)
					bot_inform.sent_to_atknin_bot( str( key ), 'v')

			out.write('\n')
			find_x_min = 100
			sam_dlinny = 0
			for i in range(j):
				if len(data['x' + str(i)])>sam_dlinny:
					sam_dlinny = len(data['x' + str(i)])
				for k in data['x' + str(i)]:
					if float(k)<find_x_min:
						find_x_min = float(k)
			find_shag = abs(float(data['x' + str(0)][0]) - float(data['x' + str(0)][1]))
			
			for i in range(sam_dlinny):
				out.write('%14.8f' % find_x_min)
				for k in range(j):
					try: 
						if find_x_min==float(data['x' + str(k)][i]):
							out.write('%14.4f' % float(data['y' + str(k)][i]))
						else:
							out.write('%14.8f' % 0)
					except: 
						out.write('%14.8f' % 0)
				out.write('\n')
				find_x_min+=find_shag
			message['path'] = '/media/converter/'+ name +'.dat'

		return JsonResponse(message)
	else:
	 	return render(
		 	request, 'general/converter.html',
		 	)	