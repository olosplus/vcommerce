# -*- coding:utf-8 -*-
from django.db import models
from cadastro.localidade.estado.models import Estado

# Create your models here.
class Cidade(models.Model):
	class Meta:
		db_table = "cidade"
		verbose_name = "Cidade"
		verbose_name_plural = "Cidades"

	cdcidade = models.CharField(max_length=10,verbose_name="Código",unique=True,db_index=True)
	nmcidade = models.CharField(max_length=250,verbose_name="Nome")
	estado = models.ForeignKey(Estado,verbose_name="Estado",null=True,blank=True)

	class Meta:
		ordering = ['nmcidade']

	def __str__(self):
		return self.nmcidade