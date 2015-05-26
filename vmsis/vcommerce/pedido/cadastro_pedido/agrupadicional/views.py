# -*- coding: utf-8 -*-
from django.shortcuts import render
from vlib.view_lib import ViewCreate, StandardFormGrid, ViewUpdate
from cadastro.produto.models import Produto
from vlib.grid import Grid
from pedido.cadastro_pedido.agrupadicional.models import AgrupAdicional, Adicionais

# Create your views here.


class GridAgrupaAdicional(Grid):
    def get_field_query_set(self, model_rel_to, field_name):
        return model_rel_to.objects.filter(idadicional=True)

    
class ViewAgrupAdicionalCreate(ViewCreate):
    def get_grid_instance(self):        
        return GridAgrupaAdicional(model = self.model)

