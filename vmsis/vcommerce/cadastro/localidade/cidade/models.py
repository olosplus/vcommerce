# -*- coding:utf-8 -*-
from django.db import models
from cadastro.localidade.pais.models import Pais
from cadastro.localidade.estado.models import Estado
from vlib.control.models import Master_empresa

class Cidade(Master_empresa):
    class Meta:
        db_table = "cidade"
        verbose_name = "Cidade"
        verbose_name_plural = "Cidade"
        ordering = ['nmcidade']

    cdcidade = models.CharField(max_length=10,verbose_name="Código",unique=True,db_index=True)
    nmcidade = models.CharField(max_length=250,verbose_name="Nome")
    pais = models.ForeignKey(Pais,verbose_name="País")
    estado = models.ForeignKey(Estado,verbose_name="Estado")

    def __str__(self):
        return self.nmcidade