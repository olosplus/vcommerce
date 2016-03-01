# -*- coding : utf-8 -*-
from django.db import models
from cadastro.produto.models import Produto
from cadastro.unimedida.models import Unimedida
from pedido.cadastro_pedido.agrupadicional.models import AgrupAdicional
from pedido.cadastro_pedido.categoria.models import Categoria
from vlib.control.models import ControleSincronizacao

# Create your models here.

class ItemCategoria(ControleSincronizacao):
    class Meta:
        db_table = "ItemCategoria"
        verbose_name = "Cardápio"
        child_models = ["ItAgrupAdicional","ComposicaoProd"]

    categoria = models.ForeignKey(Categoria, verbose_name="Categoria")
    produto = models.ForeignKey(Produto, verbose_name="Produto")
    vrvenda = models.FloatField(verbose_name="Preço")
    qtvenda = models.FloatField(verbose_name = "Quantidade")
    qtadicgratis = models.IntegerField(verbose_name = "Adicionais gratuitos")
    dsproduto = models.CharField(max_length=100,verbose_name="Descrição")

    def __str__(self):
        return self.dsproduto

class ItAgrupAdicional(ControleSincronizacao):
    class Meta:
        db_table = "itagrupadicional"
        verbose_name = "Agrupamentos de Adicionais Permitidos"
        verbose_name_plural = "Agrupamentos de Adicionais Permitidos"

    cardapio = models.ForeignKey(ItemCategoria)
    agrupadicional = models.ForeignKey(AgrupAdicional, verbose_name="Agrupamentos de Adicionais")

class ComposicaoProd(ControleSincronizacao):
	class Meta:
		db_table = "ComposicaoProd"
		verbose_name = "Composição do produto"
		verbose_name_plural = "Composições dos produtos"
	
	categoria = models.ForeignKey(ItemCategoria)
	produto = models.ForeignKey(Produto, verbose_name='Produto')
	qtcomp = models.FloatField(verbose_name="Quantidade")
	unimedida = models.ForeignKey(Unimedida,verbose_name='Unidade de medida')

