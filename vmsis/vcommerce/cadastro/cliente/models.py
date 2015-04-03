# -*- coding: utf-8 -*-
from django.db import models
from vlib.control.models import Master

choice_tipo_jfo = (('J','Jurídica'),
	('F','Física'),
	('O','Outros'))

# Create your models here.
class Cliente(Master):
    class Meta:
    	db_table = "cliente"
    	verbose_name = "Cliente"
    	verbose_name_plural = "Clientes"

    nmcliente = models.CharField(max_length=250,verbose_name="Nome",unique=True)
    nrinscjurd = models.CharField(max_length=20,verbose_name="Inscrição Jurídica")
    identificador = models.CharField(max_length=1,verbose_name="Tipo",choices=choice_tipo_jfo)

    def __str__(self):
    	return self.nmcliente