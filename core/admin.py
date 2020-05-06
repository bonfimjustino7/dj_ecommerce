from datetime import datetime

from django.contrib import admin
from django.utils.text import slugify
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import MPTTModelAdmin

from core.models import *
from poweradmin.admin import *


class TagsInline(PowerTabularInline):
    model = Tags
    extra = 1

@admin.register(Section)
class SectionAdmin(PowerModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Article)
class ArticleAdmin(PowerModelAdmin):
    list_display = ('title','author', 'section', 'dt_created', 'dt_publication', 'publicated',)
    fieldsets = (
        (None, {
           'fields': (('title', 'publicated',), 'header', 'content', 'section', 'produto')
        }),
    )
    inlines = (TagsInline, )
    raw_id_fields = ('produto',)

    def save_model(self, request, obj, form, change):
        pre_content = '<h2>%s</h2><img src="/static/img/default.jpg" style="height:150px; width:150px"/><p><b>Descrição: </b>%s</p><span><b>Preço:</b>%s</span>' % (obj.produto.name, obj.produto.descricao, obj.produto.preco)
        obj.author = request.user
        obj.slug = slugify(obj.title)
        if obj.content == '' or obj.content is None:
            obj.content = pre_content
        if obj.header == '' or obj.header is None:
            obj.header = pre_content

        if obj.publicated:
            obj.dt_publication = datetime.now()
        obj.save()

        return super().save_model(request, obj, form, change)

@admin.register(Menu)
class MenuAdmin(DjangoMpttAdmin):
    list_display = ('name', 'is_active',)
    list_editable = ('is_active',)
    item_label_field_name = 'title_for_admin'

@admin.register(Produto)
class ProdutoAdmin(PowerModelAdmin):
    list_display = ('name', 'descricao',)

    # desabilitando add e deletion para popup
    def has_add_permission(self, request):
        if request.GET.get('_popup'):
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.GET.get('_popup'):
            return False
        return True