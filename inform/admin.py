from django.contrib import admin
from inform import models

# Register your models here.
class participants_admin(admin.ModelAdmin):
	list_display = (u'LastName', u'Name', u'email', 'phone','DateTime')

admin.site.register(models.participants, participants_admin)
