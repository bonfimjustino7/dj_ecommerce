from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.db import models


class Produto(models.Model):
    name = models.CharField('Nome', max_length=200)
    preco = models.DecimalField('Preço', decimal_places=2, max_digits=10)
    descricao = models.TextField('Descrição Curta', blank=True, null=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT, null=True, blank=True)
    imagem = models.ImageField(upload_to='imgs', null=True, blank=True)
    marca = models.CharField(max_length=100, null=True, blank=True)
    modelo = models.CharField(max_length=100, null=True, blank=True)

    def produtos_estoque(self):
        count = 0
        for mov in self.movimentacao_set.all():
            count += mov.quantidade
        return count
    produtos_estoque.short_description = 'Produtos em Estoque'

    def __str__(self):
        return self.name

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def qtd_produtos(self):
        return self.produto_set.all().count()
    qtd_produtos.short_description = 'Quantidade de Produtos'

    def __str__(self):
        return self.nome

class Compra(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField('Quantidade de produtos')
    comprador = models.ForeignKey(User, on_delete=models.PROTECT)
    date_compra = models.DateTimeField('Data da Compra', auto_now_add=True)

    @property
    def valor_total(self):
        return self.produto.preco * self.quantidade


TIPO = (
    ('Entrada', 'E'),
    ('Saída', 'S'),
    ('Estorno Entrada', 'EE'),
    ('Estorno Saída', 'ES'),
)

class TipoMovimentacao(models.Model):
    tipo = models.CharField(max_length=15, choices=TIPO)
    valor = models.IntegerField()

    def __str__(self):
        return self.tipo


class Movimentacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    tipo = models.ForeignKey(TipoMovimentacao, on_delete=models.PROTECT, verbose_name='Tipo de Movimentação')
    quantidade = models.IntegerField('Quantidade Adicionada')
    dt_movimentacao = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return '%s - %s %s_%s' % (self.produto, self.tipo, self.quantidade, self.dt_movimentacao)

    class Meta:
        verbose_name = 'uma Movimentação'
        verbose_name_plural = 'Movimentações'