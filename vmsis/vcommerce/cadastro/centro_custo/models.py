# coding : utf-8
from django.db import models
from vlib.control.models import Master_empresa
from cadastro.unidade.models import Unidade

class CentroCusto(Master_empresa):
    class Meta:
    	db_table = "centro_custo"
    	verbose_name = "Centro de custo"
    	verbose_name_plural = "Centro de custos"
    	ordering = ['codigo']

    codigo = models.CharField(max_length = 30, verbose_name = "Código", unique = True)
    nome = models.CharField(verbose_name = "Nome", max_length = 100)
    unidade = models.ManyToManyField(Unidade, verbose_name = "Unidades", null=True)

    def __str__(self):
        return "%s - %s" % (self.codigo, self.nome)