# -*- coding: utf-8 -*-
from django.db import models
from cadastro.localidade.cidade.models import Cidade
from vlib.control.models import Master_empresa, ControleSincronizacao

# Create your models here.
class Bairro(Master_empresa, ControleSincronizacao):
	class Meta:
		db_table = "bairro"
		verbose_name = "Bairro"
		verbose_name_plural = "Bairros"
		ordering = ['nmbairro']

	cdbairro = models.CharField(max_length=10,verbose_name="Código",unique=True,db_index=True)
	nmbairro = models.CharField(max_length=250,verbose_name="Nome")
	cidade = models.ForeignKey(Cidade,verbose_name="Cidade")

	def __str__(self):
		return self.nmbairro