# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class books(models.Model):
	name = models.CharField(max_length=20)
	path = models.CharField(max_length=20)
	url = models.CharField(max_length=20)
	
	class Meta:
		verbose_name = u'книга'
		verbose_name_plural = u'книгы' 

	def __unicode__(self):
		return self.name.encode('utf-8')	