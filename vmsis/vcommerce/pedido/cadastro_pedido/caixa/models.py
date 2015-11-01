# coding: utf-8
from django.db import models
from cadastro.unidade.models import Unidade
from vlib.control.models import ControleSincronizacao

# Create your models here.
class Caixa(ControleSincronizacao):
    class Meta:
        db_table = "caixa"
        verbose_name = "Caixa"
        verbose_name_plural = "Caixas"
    nmcaixa = models.CharField(max_length=50, verbose_name="Nome")
    unidade = models.ForeignKey(Unidade,verbose_name="Unidade", null=True, blank=True)

    def __str__(self):
        return self.nmcaixa