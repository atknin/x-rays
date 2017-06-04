from django.contrib import admin
from library import models

# Register your models here.
class labrary_admin(admin.ModelAdmin):
	list_display = ('id',u'title', u'annotation')

class tags_admin(admin.ModelAdmin):
	list_display = (u'text',)

class author_admin(admin.ModelAdmin):
	list_display = (u'last_name',)

admin.site.register(models.labrary, labrary_admin)
admin.site.register(models.Tag, tags_admin)
admin.site.register(models.author, author_admin)
