# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class books(models.Model):
	name = models.CharField(max_length=20)
	path = models.CharField(max_length=80)
	url = models.CharField(max_length=80)
	
	class Meta:
		verbose_name = u'книга'
		verbose_name_plural = u'книги' 

	def __unicode__(self):
		return self.name.encode('utf-8')

class task(models.Model):
	text = models.CharField(max_length=1000)
	user = models.CharField(max_length=30)
	feedback = models.CharField(max_length=500, blank=True)
	status = models.BooleanField(default=False)	
	date = models.DateTimeField(auto_now_add=True, blank=True)

	class Meta:
		verbose_name = u'Задача'
		verbose_name_plural = u'Задачи' 

	def __unicode__(self):
		return self.name.encode('utf-8')	