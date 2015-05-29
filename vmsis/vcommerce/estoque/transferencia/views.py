# -*- coding: utf-8 -*-
from vlib.view_lib import ViewCreate, StandardFormGrid, ViewUpdate
from estoque.transferencia.models import Transferencia
from estoque.transferencia.itemtransf.models import Itemtransf
from estoque.lib_est.estoque import Estoque

class FormTransferencia(StandardFormGrid):
    class Meta:
        model = Transferencia
    
    def after_insert_grid_row(self, instance):
        msgErro = str()
        FunEstoque = Estoque(self.funcionario["empresa"])
        transf = Transferencia.objects.get(pk=instance.master_moviest_id)
        msgErro = FunEstoque.said_prod_est(instance.produto_id, transf.to_almoxarifado, instance.lote_old_id, instance.qtdeprod)
        if not msgErro:
            msgErro = FunEstoque.entr_prod_est(instance.produto_id, transf.from_almoxarifado, instance.lote_id, instance.qtdeprod)
        return msgErro

    def after_update_grid_row(self, instance, old_instance):
        msgErro = str()

        return msgErro

    def before_delete_grid_row(self, instance):
        msgErro = str()
        return msgErro

class ViewTransferenciaCreate(ViewCreate):
    form_class = FormTransferencia

class ViewTransferenciaUpdate(ViewUpdate):
    form_class = FormTransferencia