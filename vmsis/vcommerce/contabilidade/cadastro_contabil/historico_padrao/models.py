# coding : utf-8
from django.db import models
from vlib.control.models import Master_empresa

# Create your models here.
class HistoricoPadrao(Master_empresa):
    codigo = models.IntegerField(verbose_name = "Código", unique = True)
    nome = models.CharField(verbose_name = "Nome", unique = True, max_length = 40)
    historico = models.TextField(verbose_name = "Histórico")   
    def __str__(self):
        return "%s - %s" % (self.codigo, self.nome)