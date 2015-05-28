from django.shortcuts import render
from vlib import view_lib
from cadastro.empresa.models import Empresa
from cadastro.almoxarifado.models import Almoxarifado
from cadastro.unidade.models import Unidade
from parametro.paramgeral.models import Paramgeral
from django.core.exceptions import ValidationError
from django.forms import ModelForm

class FormEmpresa(view_lib.StandardFormGrid):
    class Meta:
        model = Empresa
    
    def save(self, commit = False):
        instance = super(FormEmpresa, self).save(commit=True)
        
        unidade = Unidade()
        setattr(unidade, 'empresa_id' , instance.id)
        setattr(unidade, 'nmrazao' , instance.nmempresa)
        setattr(unidade, 'nmfantasia' , instance.nmempresa)
        setattr(unidade, 'idtipo' , 'M')
        setattr(unidade, 'nrinscjurd' , instance.codigo)
        setattr(unidade, 'identificador' , 'J')
        setattr(unidade, 'dtcadastro' , instance.dtcadastro)
        try:
            unidade.full_clean()
        except ValidationError as e:
            raise
        else:
            unidade.save()

        almoxarifado = Almoxarifado()
        setattr(almoxarifado, 'empresa_id' , instance.id)
        setattr(almoxarifado, 'nmalmoxa' , 'Almoxarifado padrão')
        try:
            almoxarifado.full_clean()
        except ValidationError as e:
            raise
        else:
            almoxarifado.save()

        paramgeral = Paramgeral()
        setattr(paramgeral, 'empresa_id' , instance.id)
        try:
            paramgeral.full_clean()
        except ValidationError as e:
            raise
        else:
            paramgeral.save()

        return instance

# Create your views here.
class ViewEmpresa(view_lib.ViewCreate):
    form_class = FormEmpresa