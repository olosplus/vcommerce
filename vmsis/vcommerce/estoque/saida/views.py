# -*- coding: utf-8 -*-
from vlib.view_lib import ViewCreate, StandardFormGrid, ViewUpdate  
from estoque.saida.models import Saida
from estoque.itemproduto.models import Itemproduto
from estoque.lib_est.estoque import Estoque

class FormSaida(StandardFormGrid):
    class Meta:
        model = Saida

    def after_insert_grid_row(self, instance):        
        FunEstoque = Estoque(self.funcionario["empresa"])
        if FunEstoque.said_prod_est(instance.produto_id, instance.almoxarifado, instance.lote_id, instance.qtdeprod):
        	Saida.objects.get(pk=instance.master_moviest_id).delete()

    def after_update_grid_row(self, instance, old_instance):
        print(instance.qtdeprod)
        print(old_instance.qtdeprod)

    def before_delete_grid_row(self, instance):
        print('before_delete_grid_row')

class ViewSaidaCreate(ViewCreate):
    form_class = FormSaida

class ViewSaidaUpdate(ViewUpdate):
    form_class = FormSaida
