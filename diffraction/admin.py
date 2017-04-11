# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models as models_django
from diffraction import models
# Register your models here.

class anod_admin(admin.ModelAdmin):
	list_display = (u'name',)

class wavelength_admin(admin.ModelAdmin):
	list_display = (u'name', u'wavelength')

class list_of_calcs_admin(admin.ModelAdmin):
	list_display = (u'PC', u'email', u'status', u'progress')
	formfield_overrides = {
		models_django.CharField: {'widget': TextInput(attrs={'size':'100'})}}

class PC_admin(admin.ModelAdmin):
	list_display = (u'auto_increment_id', u'name', u'ip')

admin.site.register(models.anod, anod_admin)
admin.site.register(models.wavelength, wavelength_admin)
admin.site.register(models.list_of_calcs, list_of_calcs_admin)
admin.site.register(models.PC, PC_admin)
