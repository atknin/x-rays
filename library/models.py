from django.db import models

# Create your models here.
class Tag(models.Model):
    text = models.CharField(max_length=64, unique=True)
    def __str__(self):
        return 'tag {id}. {text}]'.format(
            id=self.id, text=self.text)
    class Meta:
        verbose_name = u'tag'
        verbose_name_plural = u'tags'

class author(models.Model):
    last_name_eng = models.CharField(max_length=40)
    last_name_rus = models.CharField(max_length=40)

    def __str__(self):
        return 'auth {id}. {text}]'.format(
            id=self.id, text=self.last_name_rus.encode('utf-8'))

    class Meta:
        verbose_name = u'автор'
        verbose_name_plural = u'авторы'

class labrary(models.Model):
    title = models.CharField(max_length=200)
    annotation = models.CharField(max_length=1000, null = True, blank = True)
    reference = models.CharField(max_length=1000, null = True, blank = True)
    url = models.URLField(blank = True)
    tags = models.ManyToManyField(Tag, related_name='libraries')
    file_f = models.FileField(upload_to='books/library/', blank = True)
    authors = models.ManyToManyField(author, related_name='author')
    # name = models.SlugField(max_length=200,unique=True)

    def __str__(self):
        return 'id. {name}]'.format(
            id=self.id, name=self.title.encode('utf-8'))
    class Meta:
        verbose_name = u'Литературу'
        verbose_name_plural = u'Литература'
    def __unicode__(self):
        return self.title.encode('utf-8')
