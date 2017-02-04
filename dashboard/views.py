# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from dashboard import models as dashboard_models
# Create your views here.
def dashboard(request):
	args = {}
	args['books'] = dashboard_models.books.objects.all()

	return render(
	 	request, 'dashboard/dashboard.html', args
	 	)