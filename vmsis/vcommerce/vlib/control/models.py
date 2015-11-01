# -*- coding: utf-8 -*-
from django.db import models
from cadastro.empresa.models import Empresa


class ControleSincronizacao(models.Model):
    class Meta:
        abstract = True

    dt_data_inc_sinc = models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro', 
        editable=False)
    dt_data_edt_sinc = models.DateTimeField(verbose_name='Data de cadastro', null=True,
        editable=False)  


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

from cadastro.localidade.bairro.models import Bairro

class EnderecoGenerico(models.Model):
    class Meta:
        abstract = True

    nmrua = models.CharField(max_length=200,verbose_name="Rua", null=True, blank=True)
    cdnumero = models.CharField(max_length=30,verbose_name="Número", null=True, blank=True)
    cdcep = models.CharField(max_length=10,verbose_name="CEP", null=True, blank=True)
    cdbairro = models.ForeignKey(Bairro,verbose_name="Bairro", null=True, blank=True)


