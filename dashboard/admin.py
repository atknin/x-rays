# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from dashboard import models
# Register your models here.

class books_admin(admin.ModelAdmin):
	list_display = (u'name',u'path')

class task_admin(admin.ModelAdmin):
	list_display = (u'date',u'user',u'text',u'status')


admin.site.register(models.books, books_admin)
admin.site.register(models.task, task_admin)
