# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from polarizability import models
# Register your models here.

class crystals_admin(admin.ModelAdmin):
	list_display = (u'name', u'short_name')

admin.site.register(models.crystals, crystals_admin)
