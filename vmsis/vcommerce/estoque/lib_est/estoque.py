# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Sum
from estoque.posestoque.models import Posestoque
from cadastro.produto.models import Produto
from cadastro.unimedida.models import Unimedida

class Valida(object):
	def nao_existe(self, p_parametro):
		if not p_parametro:
			return 'Parametro deve ser informado.'

class Estoque(object):
	"""
	Médotos da classe Estoque:
	- qtde_prod_est => Retorna quantidade em estoque de um determinado produto.
	- entr_prod_est => Grava quantidade de produtos no estoque (posestoque).
	"""
	valida = Valida()

	def __init__(self, empresa):
		self.empresa = empresa

	def qtde_prod_est(self, p_produto, p_almoxa, p_lote):
		"""
		Objetivo: 
			Retornar quantidade em estoque de um determinado produto.	
		Parâmetros:
		-	p_produto => Produto que deseja consultar.
		-	p_almoxa => Almoxarifado que o produto se encontra, caso esteja vazio será verificado o almoxarifado que possui quantidade.
		-	p_lote => Lote do produto, caso esteja vazio será ignorado o lote.
		"""
		if not p_produto:
			return 'Erro: Produto não foi informado.'
		if not p_almoxa:
			return 'Erro: Almoxarifado não foi informado.'
		qtde_produto = 0

		try:
			if p_lote:
				if p_almoxa:
					posicao = Posestoque.objects.filter(empresa_id=self.empresa, produto_id=p_produto, almoxarifado=p_almoxa, lote=p_lote)
				else:
					posicao = Posestoque.objects.filter(empresa_id=self.empresa, produto_id=p_produto, lote=p_lote)
			else:
				if p_almoxa:
					posicao = Posestoque.objects.filter(empresa_id=self.empresa, produto_id=p_produto, almoxarifado=p_almoxa)
				else:
					posicao = Posestoque.objects.filter(empresa_id=self.empresa, produto_id=p_produto)

			return str(posicao.aggregate(Sum('qtdeproduto'))['qtdeproduto__sum'])
		except Posestoque.DoesNotExist:
			return str(qtde_produto)

	def entr_prod_est(self, p_produto, p_almoxa, p_lote, p_qtde, p_vrprod=0):
		"""
		Objetivo: 
			Realiza entrada de produto no estoque.
		Parâmetros:
		-	p_produto => Produto que deseja consultar.
		-	p_almoxa => Almoxarifado que o produto se encontra, caso esteja vazio será verificado o almoxarifado que possui quantidade.
		-	p_lote => Lote do produto, caso esteja vazio será ignorado o lote.
		-	p_qtde => Quantidade do produto (Deve ser maior que zero).
		-	p_vrprod => Valor do produto.
		"""
		if not p_produto:
			return 'Erro: Produto não foi informado.'
		if not p_almoxa:
			return 'Erro: Almoxarifado não foi informado.'

		try:
			produto = Produto.objects.get(pk=p_produto)
			medida = Unimedida.objects.get(pk=produto.unimedida_id)
			qtfatorconv = medida.qtfatorconv
		except Unimedida.DoesNotExist:
			return 'Erro: Unidade de medida não existe.'
		except Produto.DoesNotExist:
			return 'Erro: Produto não existe.'

		try:
			if p_lote:
				posicao = Posestoque.objects.get(empresa_id=self.empresa, produto_id=p_produto, almoxarifado=p_almoxa, lote=p_lote)
			else:
				posicao = Posestoque.objects.get(empresa_id=self.empresa, produto_id=p_produto, almoxarifado=p_almoxa)
			posicao.qtdeproduto += (p_qtde*qtfatorconv)
			posicao.save()
		except Posestoque.DoesNotExist:
			if p_lote:
				posicao = Posestoque.objects.create(
					empresa_id=self.empresa,
					produto_id=p_produto,
					almoxarifado=p_almoxa,
					lote=p_lote,
					qtdeproduto=p_qtde*qtfatorconv
					)
			else:
				posicao = Posestoque.objects.create(
					empresa_id=self.empresa,
					produto_id=p_produto,
					almoxarifado=p_almoxa,
					qtdeproduto=p_qtde*qtfatorconv
					)

	def said_prod_est(self, p_produto, p_almoxa, p_lote, p_qtde, p_vrprod):
		"""
		Objetivo: 
			Realiza saída de produto no estoque.
		Parâmetros:
		-	p_produto => Produto que deseja consultar.
		-	p_almoxa => Almoxarifado que o produto se encontra, caso esteja vazio será verificado o almoxarifado que possui quantidade.
		-	p_lote => Lote do produto, caso esteja vazio será ignorado o lote.
		-	p_qtde => Quantidade do produto (Deve ser maior que zero).
		-	p_vrprod => Valor do produto.
		"""	
		return "Testando"

	def cust_prod_est(self, p_produto, p_almoxa, p_lote):
		"""
		Objetivo: 
			Consulta custo do produto no estoque.
		Parâmetros:
		-	p_produto => Produto que deseja consultar.
		-	p_almoxa => Almoxarifado que o produto se encontra, caso esteja vazio será verificado o almoxarifado que possui quantidade.
		-	p_lote => Lote do produto, caso esteja vazio será ignorado o lote.
		"""
		return "Testando"