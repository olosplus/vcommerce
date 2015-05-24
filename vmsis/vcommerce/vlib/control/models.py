# -*- coding: utf-8 -*-
from django.db import models
from cadastro.empresa.models import Empresa

class Master_endereco(models.Model):
	class Meta:
		db_table = "master_endereco"

	id = models.AutoField(primary_key=True, verbose_name="Código", editable=False)
	empresa = models.ForeignKey(Empresa, verbose_name="Empresa", null=True)
	dtcadastro = models.DateField(auto_now_add=True,null=True, verbose_name='Data de cadastro', editable=False)

from cadastro.unidade.models import Unidade

class Master_unidade(models.Model):
	class Meta:
		abstract = True

	unidade = models.ForeignKey(Unidade,verbose_name="Unidade", null=True, blank=True, editable=False)
	dtcadastro = models.DateField(auto_now_add=True, verbose_name='Data de cadastro', null=True, editable=False)

from cadastro.empresa.models import Empresa

class Master_empresa(models.Model):
	class Meta:
		abstract = True

	empresa = models.ForeignKey(Empresa,verbose_name="Empresa", null=True)
	dtcadastro = models.DateField(auto_now_add=True, verbose_name='Data de cadastro', null=True, editable=False)
