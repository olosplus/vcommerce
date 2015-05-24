# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Empresa(models.Model):
	class Meta:
		db_table = "empresa"
		verbose_name = "Empresa"
		verbose_name_plural = "Empresas"
		ordering = ['nmempresa']

	codigo = models.CharField(max_length=14,verbose_name="Código")
	nmempresa = models.CharField(max_length=255,verbose_name="Nome")
	dtcadastro = models.DateField(auto_now_add=True, verbose_name='Data de cadastro')

	def __str__(self):
		return self.nmempresa