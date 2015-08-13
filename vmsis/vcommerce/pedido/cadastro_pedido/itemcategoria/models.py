# -*- coding : utf-8 -*-
from django.db import models
from cadastro.produto.models import Produto
from pedido.cadastro_pedido.agrupadicional.models import AgrupAdicional
from pedido.cadastro_pedido.categoria.models import Categoria
# Create your models here.

class ItemCategoria(models.Model):
    class Meta:
        db_table = "ItemCategoria"
        verbose_name = "Cardápio"
        child_models = ["ItAgrupAdicional"]

    categoria = models.ForeignKey(Categoria, verbose_name="Categoria")
    produto = models.ForeignKey(Produto, verbose_name="Produto")
    vrvenda = models.FloatField(verbose_name="Preço")
    qtvenda = models.FloatField(verbose_name = "Quantidade")
    qtadicgratis = models.IntegerField(verbose_name = "Adicionais gratuitos")

    def __str__(self):
        return self.produto.nmproduto

class ItAgrupAdicional(models.Model):
    class Meta:
        db_table = "itagrupadicional"
        verbose_name = "Agrupamentos de Adicionais Permitidos"
        verbose_name_plural = "Agrupamentos de Adicionais Permitidos"

    cardapio = models.ForeignKey(ItemCategoria)
    agrupadicional = models.ForeignKey(AgrupAdicional, verbose_name="Agrupamentos de Adicionais")

