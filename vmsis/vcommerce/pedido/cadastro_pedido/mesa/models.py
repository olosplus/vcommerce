# -*- coding: utf-8 -*-
from django.db import models
from cadastro.unidade.models import Unidade

choice_tipo_idmesa = (('A','Ativa'),
	('D','Inativa'))


# Create your models here.
class Mesa(models.Model):
	class Meta:
		db_table = "mesa"
		verbose_name = "Mesa"
		verbose_name_plural = "Mesas"

	nmmesa = models.CharField(max_length=250,verbose_name="Descrição",unique=True)
	dsobsmesa = models.CharField(max_length=250,verbose_name="Observação", blank=True,null=True)
	idmesaativ = models.CharField(max_length=1,verbose_name="Situação",choices=choice_tipo_idmesa,default='A')
	unidade = models.ForeignKey(Unidade,verbose_name="Unidade", null=True, blank=True)


    