# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from dashboard import models as dashboard_models
import os
import general.bot_inform as bot_inform
from django.http import JsonResponse
import subprocess, shlex
import git
import time
# Create your views here.
def books(request):
	message = {}
	if 'pull_book' in request.POST:
		book = dashboard_models.books.objects.get(pk = request.POST['id'])
		path = '/home/atknin/env/xrays' + book.path

		# git_cmd =
		kwargs = {}
		kwargs['stdout'] = subprocess.PIPE
		kwargs['stderr'] = subprocess.PIPE
		kwargs['cwd'] = '/home/atknin/env/xrays/'
		kwargs['shell'] = True
		proc = subprocess.Popen(['git','submodule update', '--remote'], **kwargs)

		(stdout_str, stderr_str2) = proc.communicate()
		return_code = proc.wait()
		info = str(return_code)
		info += str(stderr_str2)
		info += str(stdout_str)

		# info = ''
		git_cmd = 'sudo gitbook build'
		kwargs = {}
		kwargs['stdout'] = subprocess.PIPE
		kwargs['stderr'] = subprocess.PIPE
		kwargs['cwd'] = path

		proc = subprocess.Popen(shlex.split(git_cmd), **kwargs)
		(stdout_str, stderr_str2) = proc.communicate()
		return_code = proc.wait()
		info += str(stdout_str)
		info += str(stderr_str2)
		info += str(return_code)
		# repo = git.Repo( path)
		# os.chdir(path)
		# output = subprocess.Popen(["gitbook build", path])
		# proc = subprocess.Popen(["gitbook", "build"], stdout=subprocess.PIPE, cwd=path)
		# output = proc.communicate()[0]
		# proc = subprocess.check_output(['gitbook', 'build'], cwd=path)
		# info = ' |git pull| '

		# git submodule update --remote
		# a = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, cwd=path)
		# info += a.communicate('atknin')
		# a.communicate('пароль')
		# info += str(subprocess.Popen(["gitbook build"], stdout=subprocess.PIPE, cwd=path))
		# info += str(repo.git.pull())
		# info = ''
		# info += ' |gitbook build| '+path+' '
		# info += str(os.system('gitbook build'))

		#

		message['info']= str(info)
		return JsonResponse(message)

def dashboard(request):
	if request.is_ajax():
		message = {}
		text = request.POST['text']
		current_user = request.user
		new = dashboard_models.task.objects.create(text=text)
		new.user = current_user.id
		new.save()
		message['status'] = 'success'
		return JsonResponse(message)

	args = {}
	args['books'] = dashboard_models.books.objects.all()
	args['tasks'] = dashboard_models.task.objects.all()
	if request.user.is_authenticated():
		return render(
		 	request, 'dashboard/dashboard.html', args
		 	)
	else:
		return render(
		 	request, 'general/index.html',
		 	)
