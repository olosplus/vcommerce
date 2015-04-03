# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Vatualiza(models.Model):
	class Meta:
		db_table = "vatualiza"
		verbose_name = "Atualização"
		verbose_name_plural = "Atualizações"

	resumo = models.CharField(max_length=100, verbose_name='Resumo')
	descricao = models.TextField(verbose_name='Descrição')
	versao = models.CharField(max_length=20, verbose_name='Versão')
	dtatualiza = models.DateField(verbose_name='Data de atualização')

	def __str__(self):
		return self.resumo + self.dtatualiza