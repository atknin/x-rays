# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.

class updates(models.Model):
	version = models.CharField(max_length=50)
	what_is = models.CharField(max_length=300)
	date = models.DateTimeField(auto_now_add=True, blank=True)

	class Meta:
		verbose_name = u'одновление'
		verbose_name_plural = u'обновления' 
		ordering = ['-date']

	def __unicode__(self):
		return self.name.encode('utf-8')