# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from polarizability import models as polarizability_models
from diffraction import models as diffraction_models

# Create your views here.

def diffraction(request):
	args = {}
	args['crystals'] = polarizability_models.crystals.objects.all()
	args['anod'] = diffraction_models.anod.objects.all()

	return render(
	 	request, 'diffraction/diffraction.html', args
	 	)