from django.contrib.auth.models import User
from django.db import models



class Produto(models.Model):
    name = models.CharField('Nome', max_length=200)
    preco = models.DecimalField('Preço', decimal_places=2, max_digits=10)
    descricao = models.TextField('Descrição', blank=True, null=True)

    def __str__(self):
        return self.name

class Compra(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField('Quantidade de produtos')
    comprador = models.ForeignKey(User, on_delete=models.PROTECT)
    date_compra = models.DateTimeField('Data da Compra', auto_now_add=True)

    @property
    def valor_total(self):
        return self.produto.preco * self.quantidade


TIPO = (
    ('Entrada', 'Entrada'),
    ('Saída', 'Saída'),
    ('Estorno Entrada', 'Estorno Entrada'),
    ('Estorno Saída', 'Estorno Saída'),
)

class TipoMovimentacao(models.Model):
    tipo = models.CharField(max_length=15, choices=TIPO)
    valor = models.IntegerField()

    def __str__(self):
        return self.tipo


class Movimentacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    tipo = models.ForeignKey(TipoMovimentacao, on_delete=models.PROTECT, verbose_name='Tipo de Movimentação')
    quantidade = models.IntegerField('Quantidade em estoque')
    dt_movimentacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s %s_%s' % (self.produto, self.tipo, self.quantidade, self.dt_movimentacao)

    class Meta:
        verbose_name = 'uma Movimentação'
        verbose_name_plural = 'Movimentações'