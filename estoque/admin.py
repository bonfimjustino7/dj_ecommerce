from django.contrib import admin

# Register your models here.

from estoque.models import *
from poweradmin.admin import PowerModelAdmin


@admin.register(Produto)
class ProdutoAdmin(PowerModelAdmin):
    list_display = ('id', 'name', 'descricao', 'produtos_estoque',)

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
    list_display = ('produto', 'tipo', 'quantidade', 'dt_movimentacao')

    readonly_fields = ('user',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.quantidade = obj.quantidade * obj.tipo.valor
        obj.save()

        return super().save_model(request, obj, form, change)

@admin.register(TipoMovimentacao)
class TipoMovAdmin(PowerModelAdmin):
    pass