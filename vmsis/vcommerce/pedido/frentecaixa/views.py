# -*- codaftertf-8 -*-
from django.shortcuts import render
from vlib.view_lib import ViewCreate, StandardFormGrid, ViewUpdate
from pedido.frentecaixa.models import Pedido, ItemPedido, ItAdicional
from pedido.cadastro_pedido.cardapio.models import Cardapio
from pedido.cadastro_pedido.agrupadicional.models import AgrupAdicional, Adicionais
from cadastro.produto.models import Produto

# Create your views here.
class FormFrentecaixa(StandardFormGrid):
    class Meta:
        model = Pedido
    
    def before_insert_grid_row(self, instance):
        if isinstance(instance, ItemPedido):
            cardapio = Cardapio.objects.get(pk=instance.cardapio.id)
            instance.vrvenda = cardapio.vrvenda
            instance.vrtotal = instance.qtitem * instance.vrvenda
            
    def before_update_grid_row(self, instance, old_instance):
        if isinstance(instance, ItemPedido):
            cardapio = Cardapio.objects.get(pk=instance.cardapio.id)
            instance.vrvenda = cardapio.vrvenda
            instance.vrtotal = instance.qtitem * instance.vrvenda
    	    
    def after_insert_grid_row(self, instance):
    	if isinstance(instance,ItAdicional):
            itempedido = ItemPedido.objects.get(pk=instance.itempedido.id)
            cardapio = Cardapio.objects.get(pk=itempedido.cardapio.id)
            itempedido.vrvenda = cardapio.vrvenda 
            adicionais = Adicionais.objects.get(pk=instance.item.id)
            agrupadicional = AgrupAdicional.objects.get(pk=adicionais.agrupadicional.id)
            itempedido.vrtotal = (itempedido.qtitem * cardapio.vrvenda) + (itempedido.qtitem *(agrupadicional.vragrupadic*instance.qtitem))
            itempedido.idadicional = True
            itempedido.save()

    def after_update_grid_row(self, instance,old_instance):
        if isinstance(instance,ItAdicional):
            itempedido = ItemPedido.objects.get(pk=instance.itempedido.id)
            cardapio = Cardapio.objects.get(pk=itempedido.cardapio.id)
            itempedido.vrvenda = cardapio.vrvenda 
            adicionais = Adicionais.objects.get(pk=instance.item.id)
            agrupadicional = AgrupAdicional.objects.get(pk=adicionais.agrupadicional.id)
            itempedido.vrtotal = (itempedido.qtitem * cardapio.vrvenda) + (itempedido.qtitem *(agrupadicional.vragrupadic*instance.qtitem))
            itempedido.idadicional = True
            itempedido.save()

    def save(self, commit=True):
        instance = super(FormFrentecaixa, self).save(commit=True)
        itempedido = ItemPedido.objects.filter(pedido=instance)
        vrtotal = 0
        for item in itempedido:
            vrtotal += item.vrtotal
        instance.vrpedido = vrtotal
        instance.idstatusped = 'C'
        instance.save()
        return instance
    	


class ViewFrentecaixaCreate(ViewCreate):
    form_class = FormFrentecaixa

class ViewFrentecaixaUpdate(ViewUpdate):
    form_class = FormFrentecaixa
    