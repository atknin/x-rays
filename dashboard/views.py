# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from dashboard import models as dashboard_models
import os
import general.bot_inform as bot_inform
from django.http import JsonResponse
from subprocess import Popen, PIPE
import git 

# Create your views here.
def books(request):
	message = {}
	if 'pull_book' in request.POST:
		book = dashboard_models.books.objects.get(pk = request.POST['id'])
		path = '/home/atknin/env/xrays'+book.path
		# repo = git.Repo( path)
		# os.chdir(path)

		proc = Popen(['gitbook', 'build'], stdin=PIPE, cwd=path)
		# info = ' |git pull| '

		# git submodule update --remote
		# a = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, cwd=path)
		# info += a.communicate('atknin')
		# a.communicate('vfntvfnbrf43')
		# info += str(subprocess.Popen(["gitbook build"], stdout=subprocess.PIPE, cwd=path))
		# info += str(repo.git.pull())
		# info = ''
		# info += ' |gitbook build| '+path+' '
		# info += str(os.system('gitbook build'))

		# 

		message['info']= str(proc)
		return JsonResponse(message)

def dashboard(request):
	args = {}
	args['books'] = dashboard_models.books.objects.all()
	if request.user.is_authenticated():
		return render(
		 	request, 'dashboard/dashboard.html', args
		 	)
	else:
		return render(
		 	request, 'general/index.html',
		 	)	