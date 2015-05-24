# -*- coding: utf-8 -*-
from django.db import models
from vlib.control.models import Master_unidade

class Master_moviest(Master_unidade):
    """docstring for ClassName"""
    class Meta:
        db_table = "master_moviest"

    id = models.AutoField(primary_key=True,verbose_name="Código")