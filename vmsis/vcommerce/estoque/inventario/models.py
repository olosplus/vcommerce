# -*- coding: utf-8 -*-
from django.db import models
from estoque.control.models import Master_moviest

# Create your models here.
class Inventario(Master_moviest):
    class Meta:
        db_table = "inventario"
        verbose_name = "Inventário"
        verbose_name_plural = "Inventários"
        child_models = ['estoque.itemproduto.models.Itemproduto']

    dtinventario = models.DateTimeField(verbose_name='Data do inventário')

    def __str__(self):
        return self.dtinventario