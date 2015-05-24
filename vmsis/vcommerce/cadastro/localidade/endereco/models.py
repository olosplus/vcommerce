# -*- coding: utf-8 -*-
from django.db import models
from vlib.control.models import Master_endereco
from cadastro.localidade.bairro.models import Bairro

# Create your models here.
class Endereco(models.Model):
	class Meta:
		db_table = "endereco"
		verbose_name = "Endereço"
		verbose_name_plural = "Endereços"

	nmrua = models.CharField(max_length=200,verbose_name="Rua")
	cdnumero = models.CharField(max_length=30,verbose_name="Número")
	cdcep = models.CharField(max_length=10,verbose_name="CEP")
	master = models.ForeignKey(Master_endereco)
	cdbairro = models.ForeignKey(Bairro,verbose_name="Bairro")

	def __str__(self):
		return self.cdcep