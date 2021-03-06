from django.db import models

class participants(models.Model):
	Name = models.CharField(max_length=50)
	LastName = models.CharField(max_length=50)
	email = models.EmailField(max_length=50)
	phone = models.CharField(max_length=11)
	DateTime = models.DateTimeField(auto_now_add=True, blank=True)
	ip = models.GenericIPAddressField(protocol='IPv4',blank=True,null=True)
	# client_ip = request.META['REMOTE_ADDR']

	class Meta:
		verbose_name = u'Участник лекции'
		verbose_name_plural = u'Участники лекции'
		ordering = ['-DateTime']

	def __unicode__(self):
		return self.LastName.encode('utf-8')
	def __str__(self):
		return self.LastName


class question_choose(models.Model):
	text = models.CharField(max_length=300)
	class Meta:
		verbose_name = u'Вариант ответа'
		verbose_name_plural = u'Варианты ответа'

	def __unicode__(self):
		return self.text.encode('utf-8')
	def __str__(self):
		return self.text

class types_question(models.Model):
	text = models.CharField(max_length=300)
	def __str__(self):
		return self.text

class questions(models.Model):
	text = models.CharField(max_length=300)
	types = models.ForeignKey(types_question, blank=True, null = True)
	choose = models.ManyToManyField(question_choose, blank=True)
	DateTime = models.DateTimeField(auto_now_add=True, blank=True,editable=True)
	class Meta:
		verbose_name = u'Вопрос'
		verbose_name_plural = u'Вопросы'

	def __unicode__(self):
		return self.text.encode('utf-8')
	def __str__(self):
		return self.text

class answers(models.Model):
	text = models.CharField(max_length=300, blank=True, null = True)
	number = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
	user = models.ForeignKey(participants, blank=True, null = True)
	questions = models.ForeignKey(questions)
	question_choose = models.ForeignKey(question_choose, blank=True, null = True)
	DateTime = models.DateTimeField(auto_now_add=True, blank=True)
	class Meta:
		verbose_name = u'Ответ'
		verbose_name_plural = u'Ответы'

	def __unicode__(self):
		return self.questions.text.encode('utf-8')
