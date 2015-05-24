# -*- coding: utf-8 -*-
from django.shortcuts import render
from vlib.view_lib import ViewCreate, StandardFormGrid, ViewUpdate
from cadastro.produto.models import Produto
from vlib.grid import Grid
from pedido.cadastro_pedido.agrupadicional.models import AgrupAdicional, Adicionais

# Create your views here.
class GridAgrupaAdicional(Grid):

    def get_field_query_set(self, model_rel_to, field_name):
    	print('Teste')
    	return model_rel_to.objects.filter(idadicional=True)


class ViewAgrupAdicionalCreate(ViewCreate):
    
    def get_grid(self):
        print('aa')
        return GridAgrupaAdicional(self.model)
    
#    def get_context_data(self, **kwargs):
#        context = super(ViewAgrupAdicionalCreate, self).get_context_data(**kwargs)
#        print('pt1')
#        grid = GridAgrupaAdicional(model = self.model)
#        context['grid'] = grid.grid_as_text(use_crud = False, read_only = False, dict_filter = {'id':-1});        
#        return context 

