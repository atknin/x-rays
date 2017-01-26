# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from polarizability import models as polarizability_models
from diffraction import models as diffraction_models

# Create your views here.
from django.http import HttpResponse
import general.bot_inform as bot_inform
import sys, math, cmath, os, re#, scipy # re - для работы с регулярными выражениями
# import numpy as np
from django.http import JsonResponse
import numpy as np
import time
#------для телеграма------------
from pytg import Telegram
tg = Telegram(
	telegram="/home/atknin/tg/bin/telegram-cli",
	pubkey_file="/home/atknin/tg/tg-server.pub")
receiver = tg.receiver
sender = tg.sender
#------для телеграма------------

def diffraction(request):
	args = {}
	args['crystals'] = polarizability_models.crystals.objects.all()
	args['anod'] = diffraction_models.anod.objects.all()
	return render(
	 	request, 'diffraction/diffraction.html', args
	 	)

def diffraction_scheme(request,pk_num):
	args = {}
	args['crystals'] = polarizability_models.crystals.objects.all()
	args['anod'] = diffraction_models.anod.objects.all()
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
		i = 1;
		for wave in diffraction_models.anod.objects.get(pk = request.POST['id_source']).wavelength.all():
			input_data.update({'anod'+str(i): str(wave.wavelength)})
			i+=1

		output_data['status'] = "ok"
		sender.send_msg("Atknin", str(input_data))
	else:
		output_data['status'] = "error"
	return JsonResponse(output_data)