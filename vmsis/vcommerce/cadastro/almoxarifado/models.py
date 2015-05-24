# -*- coding: utf-8 -*-
from django.db import models
from vlib.control.models import Master_endereco

# Create your models here.
class Almoxarifado(Master_endereco):
    class Meta:
    	db_table = "almoxarifado"
    	verbose_name = "Almoxarifado"
    	ordering = ['nmalmoxa']
    	verbose_name_plural = "Almoxarifados"
    	child_models = ['cadastro.localidade.endereco.models.Endereco',
    	                'cadastro.contato.models.Contato',]

    nmalmoxa = models.CharField(max_length=250,verbose_name="Descrição")

    def __str__(self):
    	return self.nmalmoxa