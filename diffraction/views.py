# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from polarizability import models as polarizability_models
from diffraction import models as diffraction_models
from datetime import datetime
# Create your views here.
from django.http import HttpResponse
import general.bot_inform as bot_inform
import sys, math, cmath, os, re#, scipy # re - для работы с регулярными выражениями
# import numpy as np
from django.http import JsonResponse
import numpy as np
import time
from django.views.decorators.csrf import csrf_exempt
#------для телеграма------------
from pytg import Telegram
tg = Telegram(
	telegram="/home/atknin/tg/bin/telegram-cli",
	pubkey_file="/home/atknin/tg/tg-server.pub")
receiver = tg.receiver
sender = tg.sender
#------/для телеграма------------

@csrf_exempt
def api(request):
	if request.method == 'GET':
		db_calc = diffraction_models.list_of_calcs.objects.create(JSON = request.POST['data'])
		db_calc.email = request.POST['id_email']
		return 1
	else:
		return render(
		 	request, 'diffraction/diffraction.html', args
		 	)


def diffraction(request):
	args = {}
	args['crystals'] = polarizability_models.crystals.objects.all()
	args['anod'] = diffraction_models.anod.objects.all()
	args['calculations'] = diffraction_models.list_of_calcs.objects.all()[::-1]
	return render(
	 	request, 'diffraction/diffraction.html', args
	 	)

def diffraction_scheme(request,pk_num):
	args = {}
	args['crystals'] = polarizability_models.crystals.objects.all()
	args['anod'] = diffraction_models.anod.objects.all()
	args['computer_online']  = diffraction_models.PC.objects.all()
	url = 'diffraction/diffraction_'+pk_num + '.html'
	return render(
	 	request, url, args
	 	)


def compute(request):
	output_data = {}
	# zero_crystal

	if request.is_ajax():
		input_data = {}
		for a in request.POST:
			input_data[a] = request.POST[a]
		del input_data['csrfmiddlewaretoken']
		input_data['id_comment_calc'] = input_data['id_comment_calc'].replace(",", ".").replace(" ", "_")
		i = 1;
		for wave in diffraction_models.anod.objects.get(pk = request.POST['id_source']).wavelength.all():
			input_data.update({'anod'+str(i): str(wave.wavelength)})
			i+=1
		output_data['status'] = "ok"
		sender.send_msg("Atknin", str(input_data))
		bot_inform.sent_to_atknin_bot(str(input_data), 'n') # проинформируем в telegramm bot
		db_calc = diffraction_models.list_of_calcs.objects.create(JSON = str(input_data))
		db_calc.email = input_data ['id_email']
		try:
			db_calc.PC = diffraction_models.PC.objects.get(name = request.POST['computer_calculate'])
		except Exception as e:
			pass
		db_calc.save()

	elif request.method == 'GET':
# проверка на наличие расчетов в базе
		if 'check' in request.GET:
			pc = request.GET['check']
			update = diffraction_models.PC.objects.get(pk = int(pc))
			update.date_here = datetime.now()
			update.save()

			no_calc = diffraction_models.list_of_calcs.objects.filter(status=False)
			if len(no_calc) == 0:
				output_data['status'] = 'Nodata'
				return JsonResponse(output_data)
			else:
				output_data['status'] = 'Nodata'
				for i in no_calc:
					if not i.PC is None:
						if i.PC.pk == int(pc):
							output_data['status'] = 'ok'
							output_data['JSON'] = i.JSON
							output_data['pk'] = i.pk

							bot_inform.sent_to_atknin_bot('PC (по запросу): '+ pc, 'v')
							return JsonResponse(output_data)
				for i in no_calc:
					if i.PC is None:
						# bot_inform.sent_to_atknin_bot('88', 'v')
						output_data['status'] = 'ok'
						output_data['JSON'] = i.JSON
						output_data['pk'] = i.pk
						# bot_inform.sent_to_atknin_bot(str(i.PC), 'v')
						i.PC = diffraction_models.PC.objects.get(pk = int(pc))
						i.save()
						bot_inform.sent_to_atknin_bot('PC: '+ pc, 'v')
						return JsonResponse(output_data)
				return JsonResponse(output_data)
# обработка успешно обработанного расчета
		elif 'complited' in request.GET:
			pc = request.GET['pc']
			update = diffraction_models.PC.objects.get(pk = int(pc))
			update.date_here = datetime.now()
			update.save()
			try:
				complited = diffraction_models.list_of_calcs.objects.get(pk = int(request.GET['complited']))
				complited.status = True
				complited.progress = 100
				complited.save()
				output_data['status'] = "complited"
				return JsonResponse(output_data)
			except Exception as e:
				output_data['status'] = "error in complited"
				output_data['e'] = str(e)
				return JsonResponse(output_data)
# обработка ошибки расчета, если ошибка произошла после передечи параметров в функцию
		elif 'error_during_compute' in request.GET:
			pc = request.GET['pc']
			update = diffraction_models.PC.objects.get(pk = int(pc))
			update.date_here = datetime.now()
			update.save()
			try:
				complited = diffraction_models.list_of_calcs.objects.get(pk = int(request.GET['error_during_compute']))
				complited.comment = str(request.GET['text_error'])
				complited.status = True
				complited.save()
				output_data['status'] = "error_during_compute"
				return JsonResponse(output_data)
			except Exception as e:
				output_data['status'] = "error in say error"
				output_data['e'] = str(e)
				return JsonResponse(output_data)

	else:
		output_data['status'] = "error"
	return JsonResponse(output_data)
