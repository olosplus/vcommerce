# -*- coding: utf-8 -*-
from django.db import models
from cadastro.unimedida.models import Unimedida
from vlib.control.models import Master_empresa, ControleSincronizacao

# Create your models here.
class Produto(Master_empresa, ControleSincronizacao):
    class Meta:
        db_table = "produto"
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nmproduto']

    posarvore = models.CharField(max_length=40,verbose_name='Arvore',null=True,blank=True,editable=False)
    nmproduto = models.CharField(max_length=200,verbose_name='Nome', unique=True)
    unimedida = models.ForeignKey(Unimedida,verbose_name='Unidade de medida')
    cdbarra = models.CharField(max_length=100,verbose_name='Código de barras',null=True, blank=True)
    idprodvenda = models.BooleanField(verbose_name='Produto de venda',default=False,blank=True) 
    idadicional = models.BooleanField(verbose_name='Adicional',default=False,blank=True)
    imgindex = models.IntegerField(verbose_name='Imagem')

    def __str__(self):
        return self.nmproduto
