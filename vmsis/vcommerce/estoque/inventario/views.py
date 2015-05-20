# -*- coding: utf-8 -*-
from vlib.view_lib import ViewCreate, StandardFormGrid, ViewUpdate
from estoque.inventario.models import Inventario
from estoque.posestoque.models import Posestoque
from estoque.itemproduto.models import Itemproduto
from estoque.lib_est.estoque import Estoque
    
class FormInventario(StandardFormGrid):
    class Meta:
        model = Inventario
    
#    def after_insert_grid_row(self, instance):
#        msgErro = ''
#
#        Posestoque.objects.filter(empresa_id=instance.empresa_id, instance.almoxarifado)
#        for 

#			iteminventario = Iteminventario.objects.create(
#				empresa_id=self.empresa,
#				produto_id=Posestoque.produto_id,
#				almoxarifado=Posestoque.almoxarifado_id,
#				qtdeproduto_old=Posestoque.qtdeproduto,
#				qtdeproduto=0,
#				master_moviest_id=self.master_moviest_ptr_id
#			)

    def after_update_grid_row(self, instance, old_instance):
        print('Foi')

class ViewInventarioCreate(ViewCreate):
    form_class = FormInventario

class ViewInventarioUpdate(ViewUpdate):
    form_class = FormInventario