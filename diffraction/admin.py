# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from diffraction import models
# Register your models here.

class anod_admin(admin.ModelAdmin):
	list_display = (u'name',)

class wavelength_admin(admin.ModelAdmin):
	list_display = (u'name', u'wavelength')

admin.site.register(models.anod, anod_admin)
admin.site.register(models.wavelength, wavelength_admin)
