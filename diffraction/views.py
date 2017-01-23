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



def compute(request):
	output_data = {}
	# zero_crystal

	if request.is_ajax():
		input_data = {}

		input_data['source_divergence_arc'] = float(request.POST['source_divergence_arc'])
		input_data['input_l_slit1'] = float(request.POST['input_l_slit1'])
		input_data['input_size_slit2'] = float(request.POST['input_size_slit2'])
		input_data['schem'] = request.POST['schem']
		input_data['input_size_slit1'] = float(request.POST['input_size_slit1'])
		input_data['input_l_slit2'] = float(request.POST['input_l_slit2'])
		input_data['id_email'] = float(request.POST['id_email'])
		
		i = 1;
		for wave in diffraction_models.anod.objects.get(pk = request.POST['id_source']).wavelength.all():
			input_data['anod'+str(i)] = str(wave.wavelength)
			i+=1

		output_data['status'] = "ok"
		sender.send_msg("Atknin", str(input_data))
	else:
		output_data['status'] = "error"
	return JsonResponse(output_data)