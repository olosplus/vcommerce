# -*- coding: utf-8 -*-
from vlib.view_lib import ViewCreate, StandardFormGrid, ViewUpdate, ConvertView
from vlib.url_lib import urlsCrud
from estoque.inventario.models import Inventario
from estoque.posestoque.models import Posestoque
from estoque.inventario.iteminvent.models import Iteminvent
from estoque.lib_est.estoque import Estoque
from django.shortcuts import redirect
from django import forms
    
class ConvertViewParam(ConvertView):
    def Update(self, MediaFiles = [],  ClassView = ViewUpdate):

        return ClassView.as_view(model = self.model, success_url = '', 
            template_name = TEMPLATE_UPDATE, MediaFiles = MediaFiles)

class FormInventario(StandardFormGrid):
    class Meta:
        model = Inventario        
    
    def save(self, commit = True):
        msgErro = ''
        instance = super(FormInventario, self).save(commit=True)

        posestoque = Posestoque.objects.filter(empresa_id=self.funcionario['empresa'], almoxarifado_id=instance.almoxarifado_id)
        for posi in posestoque:
            iteminvent = Iteminvent()

            setattr(iteminvent, 'empresa_id', posi.empresa_id)
            setattr(iteminvent, 'produto_id', posi.produto_id)
            setattr(iteminvent, 'almoxarifado', posi.almoxarifado)
            setattr(iteminvent, 'lote', posi.lote_id)
            setattr(iteminvent, 'qtdeprod_old', posi.qtdeproduto)
            setattr(iteminvent, 'qtdeprod', posi.qtdeproduto)
            setattr(iteminvent, 'master_moviest_id', instance.master_moviest_ptr_id)

            try:
                iteminvent.full_clean()
            except ValidationError as e:
                raise
            else:
                iteminvent.save()

        return instance

class FormInventarioUpd(StandardFormGrid):
    class Meta:
        model = Inventario

    def after_update_grid_row(self, instance, old_instance):
        lote_ok = True
        msgErro = str()

        try:
            if instance.lote_id:
                posicao = Posestoque.objects.get(empresa_id=instance.empresa_id, produto_id=instance.produto_id, almoxarifado=instance.almoxarifado_id, lote=instance.lote_id)
            else:
                posicao = Posestoque.objects.get(empresa_id=instance.empresa_id, produto_id=instance.produto_id, almoxarifado=instance.almoxarifado_id)
            posicao.qtdeproduto = instance.qtdeprod
            posicao.save()
        except Posestoque.DoesNotExist:
            msgErro = 'Erro: Não foi possivel atualizar o estoque. Não existe movimentação para alguns produtos.'

        return msgErro

class ViewInventarioCreate(ViewCreate):
    form_class = FormInventario

    def get_success_url(self):
        URL = urlsCrud(self.model)
        try:
           id = self.object.id
        except Exception as e:
            print(e)
        return URL.BaseUrlUpdate(CountPageBack = 1) + str(id)

class ViewInventarioUpdate(ViewUpdate):
    form_class = FormInventarioUpd