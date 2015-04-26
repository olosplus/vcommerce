# -*- coding: utf-8 -*-
from django.db import models
from vlib.control.models import Master
from vlib.control.models import Master_empresa

# Create your models here.
class Contato(Master_empresa):
	class Meta:
		db_table = "contato"
		verbose_name = "Contato"
		verbose_name_plural = "Contatos"

	nmcontato = models.CharField(max_length=200,verbose_name="Representante",blank=True)
	nrtelefone = models.CharField(max_length=30,verbose_name="Telefone")
	nrcelular = models.CharField(max_length=30,verbose_name="Celular")
	dsemail = models.CharField(max_length=150,verbose_name="E-mail")
	dsobservacao = models.CharField(max_length=400,verbose_name="Observação")
	master = models.ForeignKey(Master)

	def __str__(self):
		return self.nmcontato