# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class crystals(models.Model):

	name = models.CharField(max_length=80, unique=True)
	short_name = models.CharField(max_length=30, null=True, blank=True, \
								  help_text="chemical formula")
	crystal_system  = models.CharField(max_length=50, null=True, blank=True)
	a = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, \
								  help_text="in Angstrom unit")
	b = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, \
								  help_text="in Angstrom unit")
	c = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, \
								  help_text="in Angstrom unit")
	alfa = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, \
								  help_text="in degrees unit")
	beta = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, \
								  help_text="in degrees unit")
	gamma = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, \
								  help_text="in degrees unit")
	density = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, \
								  help_text="in gr/cm^3, example, pSi = 2.33 gr/cm^3")

	
	class Meta:
		verbose_name = u'кристалл'
		verbose_name_plural = u'кристаллы' 
		ordering = ('name',)

	def __unicode__(self):
		return self.name.encode('utf-8')