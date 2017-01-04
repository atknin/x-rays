# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from general import models
# Register your models here.

class updates_admin(admin.ModelAdmin):
	list_display = (u'version', u'date', u'what_is')

admin.site.register(models.updates, updates_admin)
