# -*- codaftertf-8 -*-
from django.shortcuts import render
from vlib.view_lib import ViewCreate, StandardFormGrid, ViewUpdate
from pedido.frentecaixa.models import Pedido, ItemPedido, ItAdicional
from pedido.cadastro_pedido.cardapio.models import Cardapio
from pedido.cadastro_pedido.agrupadicional.models import AgrupAdicional, Adicionais
from cadastro.produto.models import Produto
from estoque.lib_est.estoque import Estoque
from cadastro.unidade.models import Unidade
from pedido.cadastro_pedido.composicaoproduto.models import ComposicaoProd 
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from pedido.itemreti.models import ItemReti
from django.core.exceptions import ValidationError

# Create your views here.
class FormFrentecaixa(StandardFormGrid):
    class Meta:
        model = Pedido
    
    def before_insert_grid_row(self, instance):
        if isinstance(instance, ItemPedido):
            unidade = Unidade.objects.get(pk=instance.empresa.id)
            instance.almoxarifado = unidade.almoxpedido
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
            
        itreti = ItemReti()   
        
        setattr(itreti, 'pedido_id' , instance.id)
        
        setattr(itreti, 'almoxarifado_id' , item.almoxarifado.id)
        
        setattr(itreti, 'lote_id' , item.lote)
        
        msgErro = ''
        msgErroaux = str()
        FunEstoque = Estoque(self.funcionario["empresa"])
        for item in itempedido:
            itemcomp = ComposicaoProd.objects.filter(pk=item.cardapio.produto_id)
            if itemcomp:
                for itcomp in itemcomp:
                    setattr(itreti, 'item' , itcomp.prodcomp)
                    setattr(itreti, 'qtreti' , itcomp.qtcomp)
                    msgErroaux = FunEstoque.said_prod_est(itcomp.prodcomp.id, item.almoxarifado, item.lote_id, itcomp.qtcomp)
                    if msgErroaux :
                        msgErro =  msgErro + msgErroaux
            else:
                setattr(itreti, 'item' , item.cardapio.produto)
                setattr(itreti, 'qtreti' , item.qtitem)
                msgErroaux = FunEstoque.said_prod_est(item.cardapio.produto.id, item.almoxarifado, item.lote_id, item.qtitem)
                if msgErroaux :
                    msgErro =  msgErro + msgErroaux
            
            itadicional = ItAdicional.objects.filter(itempedido=item)
            for adcional in itadicional:
                
                itemcomp = ComposicaoProd.objects.filter(pk=adcional.adicionais.produto_id)
                if itemcomp:
                    for itcomp in itemcomp:
                        setattr(itreti, 'item' , itcomp.prodcomp)
                        setattr(itreti, 'qtreti' , itadicional.qtcomp)
                        msgErroaux = FunEstoque.said_prod_est(itcomp.prodcomp.id, item.almoxarifado, item.lote_id, itadicional.qtcomp)
                        if msgErroaux :
                            msgErro =  msgErro + msgErroaux
                else:
                    setattr(itreti, 'item' , adcional.adicionais.produto)
                    setattr(itreti, 'qtreti' , adicional.qtitem)
                    msgErroaux = FunEstoque.said_prod_est(adcional.adicionais.produto_id, item.almoxarifado, item.lote_id, adicional.qtitem)
                    if msgErroaux :
                        msgErro =  msgErro + msgErroaux
        
        if msgErro:   
            Pedido.objects.get(pk=instance.id).delete()
            return msgErro
            
        else:
            instance.save()
            
            try:
                itreti.full_clean()
            except ValidationError as e:
                raise
            else:
                itreti.save()

            return instance 
    """
    def  delete(self, commit=True):
        instance = super(FormFrentecaixa, self).delete(commit=True)
        itempedido = ItemPedido.objects.filter(pedido=instance)
        msgErro = ''
        FunEstoque = Estoque(self.funcionario["empresa"])
        for item in itempedido:
            itemcomp = ComposicaoProd.objects.filter(pk=item.cardapio.produto_id)
            if itemcomp:
                for itcomp in itemcomp:
                    msgErro =  msgErro + FunEstoque.entr_prod_est(itcomp.prodcomp.id, item.almoxarifado, item.lote_id, itcomp.qtcomp)
            else:
                msgErro =  msgErro + FunEstoque.entr_prod_est(item.cardapio.produto_id, item.almoxarifado, item.lote_id, item.qtitem)
            
        if msgErro: 
            print(msgErro)
    """
class ViewFrentecaixaCreate(ViewCreate):
    form_class = FormFrentecaixa

class ViewFrentecaixaUpdate(ViewUpdate):
    form_class = FormFrentecaixa
                                                            