# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import paramiko 
import os
from time import gmtime, strftime
commit = strftime("%Y-%m-%d %H:%M:%S", gmtime())

print(os.system('git add .'))
# print(os.system('git add -f static/icon/'))
# print(os.system('git rm --cached git_do.py'))
print(os.system('git commit -m "'+ commit + '"'))
print(os.system('git push'))




host = 'x-rays.world'
user = 'atknin'
secret = 'vfntvfnbrf43'
port = 22
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=secret, port=port)

channel = client.invoke_shell()
stdin = channel.makefile('wb')
stdout = channel.makefile('rb')
stdin.write('''
	cd env/xrays
	git pull
	touch xrays_uwsgi.ini
	''')
# git fetch --all
# 	git reset --hard origin/master

for line in stdout:
	print(line)

print('done, but not closed.')
stdout.close()
stdin.close()
client.close()
print('done and closed.')

