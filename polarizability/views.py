# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core import serializers
from polarizability import models as polarizability_models
from diffraction import models as diffraction_models

from django.http import HttpResponse
import general.bot_inform as bot_inform
import sys, math, cmath, os, re#, scipy # re - для работы с регулярными выражениями
# import numpy as np
from django.http import JsonResponse
import numpy as np
import time
import os
from polarizability import external_field, polarizab_funct
# bot_inform.sent_to_atknin_bot('wavelenght: ' + str(wavelength), 'v') # проинформируем в telegramm bot
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def api(request):
	if request.method == 'POST':
		if 'external_field' in request.POST:
			try:
				mes_field = external_field.compute(request)
				mes_normal = polarizab_funct.compute(request)
				mes_field['difference_delta'] = str(round((mes_normal['delta_precize'] - mes_field['delta_precize']),4))
				mes_field['difference_bragg'] = str(round((mes_normal['bragg_precize'] - mes_field['bragg_precize'])*3600,4))
				mes_field['difference_dprmtr_percent'] = str(round(100*(mes_normal['dprmtr_precize'] - mes_field['dprmtr_precize'])/mes_normal['dprmtr_precize'],4))
				mes_field['difference_sdvig'] = str(round((mes_normal['sdvig_precize'] - mes_field['sdvig_precize']),4))
				mes_field['difference_extintion'] = str(round((mes_normal['extintion_precize'] - mes_field['extintion_precize']),4))
			except Exception as e:
				mes_field['difference_delta'] = 'error'

			return JsonResponse(mes_field)
		else:
			return JsonResponse(polarizab_funct.compute(request))

	else:
		message['error'] = "error"
		return JsonResponse(message)


# Create your views here.
def delete(request):
	message = {}
	if request.is_ajax():
		try:
			path = os.path.realpath(os.path.dirname(sys.argv[0]))+'/polarizability/'
			crystal = polarizability_models.crystals.objects.get(pk = request.POST['id'])
			name = crystal.name
			message['status'] = 'не авторизирован, не удалено'
			if request.user.is_authenticated():
				os.remove(path+"structure/"+crystal.name+'.dat')
				crystal.delete()
				message['status'] = 'удалено'
		except Exception as e:
			message['status'] = e

	else:
		message['status'] = 'error'
	return JsonResponse(message)


def add_crystal(request):
	path = os.path.realpath(os.path.dirname(sys.argv[0]))+'/polarizability/'
	if request.is_ajax():
		message = {}
		if 'edit' in request.POST:
			edit = polarizability_models.crystals.objects.get(pk = request.POST['crystal_id'])
			edit.name = request.POST['id_name']
			edit.short_name = request.POST['id_short_name']
			edit.crystal_system = request.POST['syngony']
			edit.a = float(request.POST['id_a'])
			edit.b = float(request.POST['id_b'])
			edit.c = float(request.POST['id_c'])
			edit.alfa = float(request.POST['id_alfa'])
			edit.beta = float(request.POST['id_beta'])
			edit.gamma = float(request.POST['id_gamma'])
			edit.density = float(request.POST['id_density'])
			edit.save()
			file = open(path+"structure/"+request.POST['id_name']+'.dat', 'w')
			geom = str(request.POST['id_geom']).split(' // ')
			for i in geom:
				file.write(str(i))
				file.write("\n")
			file.close()
			message['status'] = "успешно обновлено"

		else:
			try:
				name = request.POST['id_name']
				if not polarizability_models.crystals.objects.filter(name=name).exists():
					new = polarizability_models.crystals.objects.create(name=name)
					new.short_name = request.POST['id_short_name']
					new.crystal_system = request.POST['syngony']
					new.a = float(request.POST['id_a'])
					new.b = float(request.POST['id_b'])
					new.c = float(request.POST['id_c'])
					new.alfa = float(request.POST['id_alfa'])
					new.beta = float(request.POST['id_beta'])
					new.gamma = float(request.POST['id_gamma'])
					new.density = float(request.POST['id_density'])
					new.save()

					file = open(path+"structure/"+name+'.dat', 'w')
					geom = str(request.POST['id_geom']).split(' // ')
					for i in geom:
						file.write(str(i))
						file.write("\n")
					file.close()
					message['status'] = "Успешно добавлено в базу"
				else:
					message['status'] = "Такой кристалл уже существует"

			except Exception as e:
				message['status'] = e

		return JsonResponse(message)

	elif request.method == 'POST':
		args = {}
		crystal_id = request.POST['edit_crystal']
		crystal = polarizability_models.crystals.objects.get(pk = crystal_id)
		args['edit'] = 'true'
		args['short_name'] = crystal.short_name
		args['name'] = crystal.name
		args['crystal_system'] = crystal.crystal_system
		args['a'] = crystal.a
		args['b'] = crystal.b
		args['c'] = crystal.c
		args['alfa'] = crystal.alfa
		args['beta'] = crystal.beta
		args['gamma'] = crystal.gamma
		args['density'] = crystal.density
		args['crystal_id'] = crystal_id

		path = os.path.realpath(os.path.dirname(sys.argv[0]))+'/polarizability/'
		lines = open(path+"structure/"+crystal.name+'.dat', 'r').read().split('\n')
		a = ''
		for line in lines:
			if len(line.split())>1:
				a += line + '//'
		args['crystalGeom'] = a

		return render(
		 	request, 'polarizability/add_crystal.html', args
		 	)
	else:
		return render(
		 	request, 'polarizability/add_crystal.html'
		 	)

def compute(request):
	message = {}
	message['status'] = ''
	bot_inform.sent_to_atknin_bot(str(request), 'v')
	if request.is_ajax():
		input_data = request.POST
		if 'external_field' in request.POST:
			try:
				mes_field = external_field.compute(input_data)
				mes_normal = polarizab_funct.compute(input_data)
				mes_field['difference_delta'] = str(round((mes_normal['delta_precize'] - mes_field['delta_precize']),4))
				mes_field['difference_bragg'] = str(round((mes_normal['bragg_precize'] - mes_field['bragg_precize'])*3600,4))
				mes_field['difference_dprmtr_percent'] = str(round(100*(mes_normal['dprmtr_precize'] - mes_field['dprmtr_precize'])/mes_normal['dprmtr_precize'],4))
				mes_field['difference_sdvig'] = str(round((mes_normal['sdvig_precize'] - mes_field['sdvig_precize']),4))
				mes_field['difference_extintion'] = str(round((mes_normal['extintion_precize'] - mes_field['extintion_precize']),4))
			except Exception as e:
				mes_field['difference_delta'] = 'error'

			return JsonResponse(mes_field)
		else:
			return JsonResponse(polarizab_funct.compute(input_data))
	else:
		message['error'] = "error"
		return JsonResponse(message)



def polarizability(request):
	args = {}
	args['crystals'] = polarizability_models.crystals.objects.all()
	args['lab_source'] = diffraction_models.wavelength.objects.all()

	return render(
	 	request, 'polarizability/polarizability.html', args
	 	)
