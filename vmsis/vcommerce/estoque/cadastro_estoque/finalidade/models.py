# -*- coding: utf-8 -*-
from django.db import models
from cadastro.unidade.models import Unidade

# Create your models here.
class Finalidade(models.Model):
	class Meta:
		db_table = "finalidade"
		verbose_name = "Finalidade"
		verbose_name_plural = "Finalidades"

	descricao = models.CharField(max_length=150,verbose_name="Descrição",blank=True)
	unidade = models.ForeignKey(Unidade,verbose_name="Unidade")

	def __str__(self):
		return self.descricao