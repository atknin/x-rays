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
	message = {}
	message['instrument'] = 'diffraction'
	# zero_crystal
	# scheem = request.POST['scheem']
	for mm in request.POST:
		sender.send_msg(mm, str(message))
	# scheem = float(request.POST['scheem'])

	if request.is_ajax():
		message['status'] = "ok"
		
	else:
		message['status'] = "error"
	return JsonResponse(message)