# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
# Create your models here.
import datetime
from django.utils.timezone import utc

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

class PC(models.Model):
	name = models.CharField(max_length=20)
	auto_increment_id = models.AutoField(primary_key=True)
	ip = models.CharField(max_length=50, null=True, blank = True)
	date_here = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = u'Компьютер'
		verbose_name_plural = u'Компьютеры' 

	def __unicode__(self):
		return self.name.encode('utf-8')

	def get_time_diff(self):
		now = datetime.datetime.utcnow().replace(tzinfo=utc)  # Needed to convert time to a datetime object
		timediff = now - self.date_here
		seconds = timediff.total_seconds() % 60
		if seconds>3600:
			return u'занят или отсутсвует'
		else:
			return u'в работе'
		 

class list_of_calcs(models.Model):
	JSON = models.CharField(max_length=1000)
	status = models.BooleanField(default=False)
	email = models.EmailField(max_length=100)
	data_start = models.DateTimeField(auto_now_add=True, blank=True)
	progress = models.PositiveSmallIntegerField(default=0)
	PC = models.ForeignKey(PC, blank = True, null = True)

	class Meta:
		verbose_name = u'Расчет'
		verbose_name_plural = u'Расчеты' 

	def __unicode__(self):
		return self.name.encode('utf-8')
			