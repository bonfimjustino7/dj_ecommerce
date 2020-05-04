from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey

from smart_selects.db_fields import ChainedForeignKey

class ItemManager(models.Manager):
    use_for_related_fields = True

    def active(self):
        return self.get_query_set().filter(is_active=True)

class Section(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField('Slug', max_length=250, unique=True, db_index=True, blank=True)
    slug_conf = {'field': 'slug', 'from': 'title'}

    class Meta:
        verbose_name = 'Sessão'
        verbose_name_plural = 'Sessões'

    def __str__(self):
        return self.title

class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField('Título', max_length=120)
    header = RichTextUploadingField('Chamada')
    content = RichTextUploadingField('Conteúdo')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    dt_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField('Slug', max_length=250, unique=True, db_index=True, blank=True)
    slug_conf = {'field': 'slug', 'from': 'title'}
    preco = models.FloatField('Preço')
    qtd_estoque = models.IntegerField('Quantidade em Estoque', default=0)

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
    title = models.CharField('Nome', max_length=100)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    dt_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Tag (Palavras Chaves)'
        verbose_name_plural = 'Tags (Palavras Chaves)'

class Compra(models.Model):
    produto = models.ForeignKey(Article, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    comprador = models.ForeignKey(User, on_delete=models.PROTECT)
    date_compra = models.DateTimeField('Data da Compra', auto_now_add=True)

    @property
    def valor_total(self):
        return self.produto.preco * self.quantidade

class Menu(MPTTModel):
    name = models.CharField(u'Nome', max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'Pai', on_delete=models.SET_NULL)
    link = models.CharField(u'URL', max_length=250, null=True, blank=True)
    section = models.ForeignKey('Section', null=True, blank=True, verbose_name=u'Seção', on_delete=models.SET_NULL)
    article = ChainedForeignKey(
        Article,
        chained_field='section',
        chained_model_field='section',
        show_all=False,
        auto_choose=False,
        null=True,
        blank=True,
        default=None,
        verbose_name=u'Artigo',
        on_delete=models.SET_NULL
    )
    is_active = models.BooleanField(u'Está ativo?', default=True)

    objects = ItemManager()

    def __str__(self):
        return self.name

    def get_link(self):
        link = None
        if self.link:
            link = self.link
        elif self.article:
            link = self.article.get_absolute_url()
        elif self.section:
            link = self.section.get_absolute_url()
        return link