from django.contrib import admin
from inform import models

# Register your models here.
class participants_admin(admin.ModelAdmin):
	list_display = (u'LastName', u'Name', u'email', 'phone','DateTime')

class questions_admin(admin.ModelAdmin):
	list_display = (u'text', 'DateTime')

class question_choose_admin(admin.ModelAdmin):
	list_display = (u'text', )

class answers_admin(admin.ModelAdmin):
	list_display = (u'user', u'questions',u'question_choose','DateTime')

admin.site.register(models.participants, participants_admin)
admin.site.register(models.questions, questions_admin)
admin.site.register(models.question_choose, question_choose_admin)
admin.site.register(models.answers, answers_admin)
