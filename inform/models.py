from django.db import models

class participants(models.Model):
	Name = models.CharField(max_length=50)
	LastName = models.CharField(max_length=50)
	email = models.EmailField(max_length=50)
	phone = models.CharField(max_length=11)
	DateTime = models.DateTimeField(auto_now_add=True, blank=True)

	class Meta:
		verbose_name = u'Участник лекции'
		verbose_name_plural = u'Участники лекции'
		ordering = ['-DateTime']

	def __unicode__(self):
		return self.name.LastName('utf-8')
