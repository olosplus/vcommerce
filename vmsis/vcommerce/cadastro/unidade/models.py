# -*- coding: utf-8 -*-
from django.db import models 
from vlib.control.models import Master

choice_tipo = (('M','Matriz'),
	('F','Filial'))

choice_tipo_jfo = (('J','Jurídica'),
	('F','Física'),
	('O','Outros'))

# Create your models here.
class Unidade(Master):
    class Meta:
    	db_table = "unidade"
    	verbose_name = "Unidade"
    	verbose_name_plural = "Unidades"

    nmrazao = models.CharField(max_length=255,verbose_name="Razão Social")
    nmfantasia = models.CharField(max_length=255,verbose_name="Nome Fantasia")
    idtipo = models.CharField(max_length=1,verbose_name="Tipo de Unidade",choices=choice_tipo)
    nrinscjurd = models.CharField(max_length=20,verbose_name="Inscrição Jurídica")
    identificador = models.CharField(max_length=1,verbose_name="Tipo",choices=choice_tipo_jfo, default = 'J')
    dtcadastro = models.DateField(auto_now_add=True, verbose_name='Data de cadastro')

    def __str__(self):
    	return self.nmfantasia