# -*- coding: utf-8 -*-
from django.db import models
from django.db import models
from vlib.control.models import Master_empresa, ControleSincronizacao

choice_tipo_ativ = (('A','Ativa'), ('D','Inativa'))

# Create your models here.
class Cartao_Bandeira(Master_empresa, ControleSincronizacao):
    class Meta:
        db_table = "cartao_bandeira"
        verbose_name = "Bandeiras de Cartão"
        verbose_name_plural = "Bandeiras de Cartão"

    nmbandeira = models.CharField(max_length=100, verbose_name="Bandeira")
    qtdias_cred = models.IntegerField(verbose_name="Dias para recebimento - Crédito")
    qtdias_deb = models.IntegerField(verbose_name="Dias para recebimento - Débito")
    idativo = models.CharField(max_length=1,verbose_name="Situação",choices=choice_tipo_ativ,default='A')

    def __str__(self):
        return self.nmbandeira