# coding: utf-8
from django.db import models
from vlib.control.models import Master_empresa

# Create your models here.
class TipoEscrituracaoContabil(Master_empresa):
    tipo = models.CharField(verbose_name = "Tipo", max_length = 1)
    descricao = models.CharField(verbose_name = "Descrição", max_length = 100)
    def __str__(self):
        return self.descricao