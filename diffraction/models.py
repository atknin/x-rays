# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
# Create your models here.
class wavelength(models.Model):
	name = models.CharField(max_length=20)
	wavelength = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True, \
								  help_text="in Angstrom unit")
	class Meta:
		ordering = ('name',)
		verbose_name = u'длина'
		verbose_name_plural = u'длины' 
		
	def __unicode__(self):
		return self.name.encode('utf-8')

	def __str__(self):            
		return self.name		

class anod(models.Model):
	name = models.CharField(max_length=20)
	wavelength =  models.ManyToManyField(wavelength)

	class Meta:
		verbose_name = u'Анод'
		verbose_name_plural = u'Аноды' 

	def __unicode__(self):
		return self.name.encode('utf-8')	