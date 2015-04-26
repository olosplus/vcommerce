# -*- coding: utf-8 -*-
from django.db import models
from cadastro.unidade.models import Unidade
#from vlib.control.models import Master_unidade

class Master_moviest(models.Model):
    """docstring for ClassName"""
    class Meta:
        db_table = "master_moviest"

    id = models.AutoField(primary_key=True,verbose_name="Código")
    unidade = models.ForeignKey(Unidade,verbose_name="Unidade",null=True)