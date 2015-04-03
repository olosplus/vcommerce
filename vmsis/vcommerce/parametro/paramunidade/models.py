# -*- coding: utf-8 -*-
from django.db import models
from cadastro.unidade.models import Unidade

choice_marcado = (('S','Sim'),
	('N','Não'))

# Create your models here.
class Paramunidade(models.Model):
    class Meta:
    	db_table = "paramunidade"
    	verbose_name = "Parâmetro por unidade"
    	verbose_name_plural = "Parâmetros por unidades"

    idutilinve = models.CharField(max_length=1,verbose_name="Utiliza inventário",choices=choice_marcado)
    unidade = models.ForeignKey(Unidade,verbose_name="Unidade")