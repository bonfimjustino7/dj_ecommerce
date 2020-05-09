from django.contrib import admin

# Register your models here.

from estoque.models import *
from poweradmin.admin import PowerModelAdmin


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

@admin.register(Compra)
class CompraAdmin(PowerModelAdmin):
    pass

@admin.register(Movimentacao)
class MovimentacaoAdmin(PowerModelAdmin):
    pass