# -*- coding: utf-8 -*- 
from django.db import models
from vlib.control.models import Master_empresa

choice_marcado = (('S','Sim'),
	('N','Não'))

# Create your models here.
class Paramgeral(Master_empresa):
    class Meta:
        db_table = "paramgeral"
        verbose_name = "Parâmetro geral"
        verbose_name_plural = "Parâmetros gerais"

    TextoLivre = models.CharField(max_length = 100, verbose_name = "Teste", blank=True, null=True, default="parametro")
