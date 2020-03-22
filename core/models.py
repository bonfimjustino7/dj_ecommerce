from django.conf import settings
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Section(models.Model):
    title = models.CharField(max_length=120)

    class Meta:
        verbose_name = 'Sessão'
        verbose_name_plural = 'Sessões'

    def __str__(self):
        return self.title

class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    header = RichTextUploadingField()
    content = RichTextUploadingField()
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    dt_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField('Slug', max_length=250, unique=True, db_index=True, blank=True)

    class Meta:
        verbose_name = 'Artigo'
        verbose_name_plural = 'Artigos'

    def __str__(self):
        return self.title

    def first_image(self):
        images = self.get_images()
        if images:
            return images[0]

class Tags(models.Model):
    title = models.CharField(max_length=100)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    dt_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'