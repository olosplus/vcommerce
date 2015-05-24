# -*- coding: utf-8 -*-
from django.db import models 
from vlib.control.models import Master_endereco
from cadastro.almoxarifado.models import Almoxarifado

choice_tipo = (('M','Matriz'),
	('F','Filial'))

choice_tipo_jfo = (('J','Jurídica'),
	('F','Física'),
	('O','Outros'))

class Unidade(Master_endereco):
    class Meta:
        db_table = "unidade"
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"
        ordering = ['nmfantasia']
        child_models = ['cadastro.localidade.endereco.models.Endereco',
                        'cadastro.contato.models.Contato']        

    nrinscjurd = models.CharField(max_length=20,verbose_name="Inscrição Jurídica")
    nmrazao = models.CharField(max_length=255,verbose_name="Razão Social")
    nmfantasia = models.CharField(max_length=255,verbose_name="Nome Fantasia")
    idtipo = models.CharField(max_length=1,verbose_name="Tipo de Unidade",choices=choice_tipo)
    identificador = models.CharField(max_length=1,verbose_name="Tipo",choices=choice_tipo_jfo, default = 'J')
    almoxarifado = models.ManyToManyField(Almoxarifado,verbose_name="Almoxarifado", null=True)

    def __str__(self):
        return self.nmfantasia