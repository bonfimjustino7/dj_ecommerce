from django.contrib import admin
from core.models import *
from poweradmin.admin import *

class TagsInline(PowerTabularInline):
    model = Tags
    extra = 1

class SectionAdmin(PowerModelAdmin):
    list_display = ('title',)


class ArticleAdmin(PowerModelAdmin):
    list_display = ('title','author', 'section', 'dt_created')
    fields = ('title', 'header', 'content', 'section')
    inlines = (TagsInline, )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

admin.site.register(Article, ArticleAdmin)
admin.site.register(Section, SectionAdmin)