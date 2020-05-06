import re

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils.html import strip_tags
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

    def have_perm(self, user):
        if not self.permissao_set.count():
            return True
        if user.is_superuser:
            return True
        if user.groups.filter(pk__in=self.permissao_set.values_list('pk', flat=True)).exists():
            return True
        return False

    def get_absolute_url(self):
        # return reverse('section', kwargs={'slug': self.slug})
        return ''

    def __str__(self):
        return self.title

class Produto(models.Model):
    name = models.CharField('Nome', max_length=200)
    preco = models.DecimalField('Preço', decimal_places=2, max_digits=10)
    descricao = models.TextField('Descrição', blank=True, null=True)
    qtd_estoque = models.IntegerField('Quantidade em Estoque', default=0)

    def __str__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Autor')
    title = models.CharField('Título', max_length=120)
    header = RichTextUploadingField('Chamada', null=True, blank=True, help_text='*O conteúdo pré-inscrito foi baseado no produto selecionado')
    content = RichTextUploadingField('Conteúdo', null=True, blank=True, help_text='*O conteúdo pré-inscrito foi baseado no produto selecionado.')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Sessão')
    dt_created = models.DateTimeField('Data de criação', auto_now_add=True)
    slug = models.SlugField('Slug', max_length=250, unique=True, db_index=True, blank=True)
    slug_conf = {'field': 'slug', 'from': 'title'}
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True, blank=True)
    publicated = models.BooleanField('Publicado', default=False, help_text='Marque a caixa acima se quiser publicar este post.')
    dt_publication = models.DateTimeField('Data de publicação', null=True, blank=True)

    class Meta:
        verbose_name = 'Artigo'
        verbose_name_plural = 'Artigos'

    def __str__(self):
        return self.title

    def get_images(self):
        rex = re.compile(r'(<img )(.*)(src=")([a-zA-Z0-9- _/\./:]*)(".*)(>)')
        images = []
        for img_rex in rex.findall(self.header):
            images.append(img_rex[3])
        for img_rex in rex.findall(self.content):
            images.append(img_rex[3])
        return images

    def first_image(self):
        images = self.get_images()
        if images:
            return images[0]

    def have_perm(self, user):
        if user.is_superuser or not self.sections.count():
            return True
        for section in self.sections.all():
            if not section.permissao_set.count():
                return True
            if not user.groups.filter(pk__in=section.permissao_set.values_list('pk', flat=True)).exists():
                return False
        return True

    def get_absolute_url(self):
        if str(self.pk) == self.slug:
            return strip_tags(self.content)
        return reverse('post', kwargs={'slug': self.slug})

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

    def have_perm(self, user):
        if self.parent:
            return self.parent.have_perm(user)
        if self.section:
            return self.section.have_perm(user)
        if self.article:
            return self.article.have_perm(user)
        return True

    @property
    def title_for_admin(self):
        return '%s %s' % (self.pk, self.name)