# -*- coding: utf-8 -*-
from django.shortcuts import render
from vlib.view_lib import ViewCreate, StandardFormGrid, ViewUpdate
from cadastro.produto.models import Produto
from vlib.grid import Grid as Grade
from pedido.cadastro_pedido.agrupadicional.models import AgrupAdicional, Adicionais

# Create your views here.

class GridAgrupaAdicional(Grade):
    def __init__(self, model, parent_model = None, parent_pk_value = -1, title = str()):

        self.model = model
        self.parent_model = parent_model
        self.parent_pk_value = parent_pk_value
        self.title = title


    def get_field_query_set(self, model_rel_to, field_name):
        print('Teste')
        return model_rel_to.objects.filter(idadicional=True)
    


class ViewAgrupAdicionalCreate(ViewCreate):
    def get_grid_instance(self):        
        g = GridAgrupaAdicional(model = self.model)
        return g

