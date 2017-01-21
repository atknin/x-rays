# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.
def dashboard(request):
	# args = {}
	# args['crystals'] = polarizability_models.crystals.objects.all()
	# args['lab_source'] = diffraction_models.wavelength.objects.all()

	return render(
	 	request, 'dashboard/dashboard.html'
	 	)