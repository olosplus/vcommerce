from django.shortcuts import render
from vlib.view_lib import ViewCreate, StandardFormGrid, ViewUpdate
from pedido.itemreti.models import ItemReti
from estoque.lib_est.estoque import Estoque

# Create your views here.
class FormItemreti(StandardFormGrid):
    class Meta:
        model = ItemReti
    
    def save(self, commit=False):
        print('pt1')
        instance = super(FormItemreti, self).save(commit=True)
        msgErro = ''
        FunEstoque = Estoque(self.funcionario["empresa"])
        msgErro =  msgErro + FunEstoque.said_prod_est(instance.item.id, instance.almoxarifado, instance.lote, instance.qtreti)
        if msgErro:
            print(msgErro)    
            return msgErro


class ViewItemretiCreate(ViewCreate):
    form_class = FormItemreti

class ViewItemretiUpdate(ViewUpdate):
    form_class = FormItemreti