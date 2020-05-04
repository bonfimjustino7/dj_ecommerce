from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

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
    list_display = ('title','author', 'section', 'dt_created')
    fields = ('title', 'header', 'content', 'section', 'preco', 'qtd_estoque',)
    inlines = (TagsInline, )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

@admin.register(Menu)
class MenuAdmin(DjangoMpttAdmin):
    list_display = ('name', 'is_active',)
    list_editable = ('is_active',)
