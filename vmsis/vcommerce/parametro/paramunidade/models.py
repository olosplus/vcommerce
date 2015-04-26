# -*- coding: utf-8 -*-
from django.db import models
from vlib.control.models import Master_unidade

choice_marcado = (('S','Sim'),
	('N','Não'))

# Create your models here.
class Paramunidade(Master_unidade):
    class Meta:
    	db_table = "paramunidade"
    	verbose_name = "Parâmetro por unidade"
    	verbose_name_plural = "Parâmetros por unidades"

    idutilinve = models.CharField(max_length=1,verbose_name="Utiliza inventário",choices=choice_marcado)