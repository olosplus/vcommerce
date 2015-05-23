# -*- coding: utf-8 -*-
from django.shortcuts import render
from vlib.view_lib import ViewCreate, StandardFormGrid, ViewUpdate
from pedido.frentecaixa.models import Pedido, ItemPedido
from pedido.cadastro_pedido.cardapio.models import Cardapio

# Create your views here.
class FormFrentecaixa(StandardFormGrid):
    class Meta:
        model = Pedido
    
    def before_insert_grid_row(self, instance):
    	print('passou')
    	cardapio = Cardapio.objects.filter(cardapio_id=instance.cardapio_id)
    	self.vrvenda = cardapio.vrvenda
    	self.vrtotal = self.qtitem * self.vrvenda

class ViewFrentecaixaCreate(ViewCreate):
    form_class = FormFrenteCaixa
