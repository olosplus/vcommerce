# -*- coding: utf-8 -*-
from vlib.view_lib import ViewCreate, StandardFormGrid, ViewUpdate
from estoque.entrada.models import Entrada
from estoque.itemproduto.models import Itemproduto
from estoque.lib_est.estoque import Estoque

class FormEntrada(StandardFormGrid):
    class Meta:
        model = Entrada
    
    def after_insert_grid_row(self, instance):
        msgErro = str()
        FunEstoque = Estoque(self.funcionario["empresa"])
        msgErro = FunEstoque.entr_prod_est(instance.produto_id, instance.almoxarifado, instance.lote_id, instance.qtdeprod)
        if msgErro:
        	Entrada.objects.get(pk=instance.master_moviest_id).delete()
        return msgErro

    def after_update_grid_row(self, instance, old_instance):
        lote_ok = True
        msgErro = str()
        FunEstoque = Estoque(self.funcionario["empresa"])

        qtdetemp = FunEstoque.qtde_prod_est(old_instance.produto_id, old_instance.almoxarifado, old_instance.lote_id)

        if instance.lote_id:
            if not(instance.lote_id == old_instance.lote_id):
                lote_ok = False
        if (instance.produto_id == old_instance.produto_id) and (instance.almoxarifado == old_instance.almoxarifado) and (utlote):
            if (qtdetemp - instance.qtdeprod + old_instance.qtdeprod) < 0:
                msgErro = 'Erro: Quantidade em estoque é insuficiente para a realizar a alteração.'
        if not msgErro:
            msgErro = FunEstoque.said_prod_est(old_instance.produto_id, old_instance.almoxarifado, old_instance.lote_id, old_instance.qtdeprod)
            if not msgErro:
                msgErro = FunEstoque.entr_prod_est(instance.produto_id, instance.almoxarifado, instance.lote_id, instance.qtdeprod)

        return msgErro

    def before_delete_grid_row(self, instance):
        msgErro = str()
        FunEstoque = Estoque(self.funcionario["empresa"])
        msgErro = FunEstoque.said_prod_est(instance.produto_id, instance.almoxarifado, instance.lote_id, instance.qtdeprod)
        return msgErro

class ViewEntradaCreate(ViewCreate):
    form_class = FormEntrada

class ViewEntradaUpdate(ViewUpdate):
    form_class = FormEntrada