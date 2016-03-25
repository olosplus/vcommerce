import json
from django.core.exceptions import ValidationError
from django.core import serializers
from django.http import HttpResponse
from django.db import models
from vlib.libs import lib_auxiliar
from django.db import IntegrityError
from django.db.models import Q
from django.db import transaction

# Create your views here.
class Autenticacao(object):
    def __init__(self, usuario, senha):
        self.usuario = usuario
        self.senha = senha
    
    def autenticado(self):
        #dados fixos até ajustar a questão da criptografia
        if (self.senha == 'masterVMSIS123v') and (self.usuario == 'vmsismaster'):
            return True
        else:
            return False

class SincronizacaoBase(object):
    def __init__(self, usuario, senha):
        self.usuario = usuario
        self.senha = senha        

    def Autenticado(self):
        aut = Autenticacao(self.usuario, self.senha)
        return aut.autenticado()

class DownloadModel(SincronizacaoBase):
    def __init__(self, usuario, senha, model, DataUltimaSinc):
        super(DownloadModel, self).__init__(usuario = usuario, senha = senha)
        self.fields = []
        self.filtro = {}
        self.model = model
        self.DataUltimaSinc = DataUltimaSinc            

    def GetDataAsXML(self):
        if not self.Autenticado():
            return HttpResponse('Login error')
        try:
            if self.filtro:
                condicao = json.loads(self.filtro)
                objs = self.model.objects.filter(Q(dt_data_inc_sinc__gte=self.DataUltimaSinc) | 
                    Q(dt_data_edt_sinc__gte=self.DataUltimaSinc)).filter(**condicao)
            else:
                objs = self.model.objects.filter(Q(dt_data_inc_sinc__gte=self.DataUltimaSinc) | 
                    Q(dt_data_edt_sinc__gte=self.DataUltimaSinc))
            
            if self.fields:
                query = serializers.serialize("xml", objs, 
                    fields = tuple(self.fields))
            else:
                query = serializers.serialize("xml", objs)
        except Exception as e:
            return HttpResponse(e)
        
        return HttpResponse(query)



class UploadModel(SincronizacaoBase):
#''' {"model":"nome","module":"mo" "rws":[{"campo1":"valor", "campo1":"valor", 
#    "model_child":[ {"model":"nome", "module":"mo" "parent_field":"nome",
#      "rws":[{"campo1":"value"}]  }]   }] }'''    

    def __init__(self, usuario, senha):
        super(UploadModel, self).__init__(usuario, senha)
        self.str_lista_id_desktop = str()
    
    def SaveJson(self, json_data, parent_id):
        if not self.Autenticado():
            return HttpResponse('Error|Login error')
        
        try:
            model = lib_auxiliar.get_model_by_string(json_data["module"], json_data["model"])
            
            parent_field = None
            
            if "parent_field" in json_data.keys():
                parent_field = json_data["parent_field"]
            
            chaves = str();
            if "chaves" in json_data.keys():
                chaves = json_data["chaves"]
            
            rows = json_data["rws"]
    
            for row in rows:
                self.str_lista_id_desktop += "|model=" + model.__name__ + ";"
                
                id_ou_erro = self.SaveRow(model = model, row = row, chaves = chaves, 
                    parent_field = parent_field, parent_id = parent_id)
    
                #retorna mensagem de erro caso não haja sucesso
                if type(id_ou_erro) == str:
                    return HttpResponse("Error|" + id_ou_erro)
                
                if "model_child" in row.keys():
                    for child in row["model_child"]:
                        self.SaveJson(json_data = child, parent_id = id_ou_erro)
        except Exception as e:
            HttpResponse('Error|%s' % str(e))
        return HttpResponse("success|" + self.str_lista_id_desktop)
    
    #chaves deve vir no formato 'chavecomposta1,chavecomposta2|chavesimples'
    #agrupamento por pipe quer dizer que os campos são de chave composta
    def GetModelExistente(self, chaves, class_model, json_registro):
        mod = None
        if chaves:
            lista_chaves = chaves.split("|")
        
            for chave in lista_chaves:
        
                if chave == str():
                    continue
                
                filtro_chave = {}
                lista_campo_caves = chave.split(",")
                
                for campo_chave in lista_campo_caves: 
                    if campo_chave == str():
                        continue                            
                
                    if campo_chave in json_registro.keys():
                        filtro_chave.update({campo_chave : json_registro[campo_chave]})  
                
                try:
                    mod = class_model.objects.get(**filtro_chave)
                except class_model.DoesNotExist:
                    mod = None
                
                if mod:
                    break
        
        if not mod:
            mod = class_model()
        
        return mod

    def GetFkModel(self, field_obj):
        
        if field_obj.__class__ == models.ForeignKey:
            mod_pai = field_obj.rel.to                        
        else:
            mod_pai = None
        
        return mod_pai

    def GetIdModelPaiOuValorFiltro(self, field_obj, nome_campo_filtro, valor_filtro):
        try:
            valor_retorno = valor_filtro   
    
            if valor_filtro:     
                mod_pai = mod_pai = self.GetFkModel(field_obj = field_obj)
                
                if mod_pai:
                    #por algum motivo o método hasattr não funciona para o campo id_desktop, então preciso fazer essa gambiarra
                    mod_p = mod_pai()            
                    if nome_campo_filtro in mod_p.__dict__.keys():        
                        where = {nome_campo_filtro:valor_filtro}
                        try:
                            valor_retorno = mod_pai.objects.get(**where).id
                        except mod_pai.DoesNotExist:
                            valor_retorno = valor_filtro
            
            return self.GetValorTratado(field_obj = field_obj, valor = valor_retorno)    
        except Exception as e:
            print(e)
         
    def GetNomeColunaBd(self, field_obj):
        return field_obj.get_attname_column()[0]        

    def GetValorTratado(self, field_obj, valor):
        valor_retorno = valor

        if field_obj.__class__ in (models.IntegerField, models.BigIntegerField, \
            models.PositiveIntegerField, models.PositiveSmallIntegerField, \
            models.SmallIntegerField, models.DecimalField, models.FloatField) and \
            valor == str():
        
            valor_retorno = None
        elif field_obj.__class__ == models.BooleanField:
            if valor == 0:
                valor_retorno = False
            elif valor == 1:
                valor_retorno = True

        return valor_retorno   


    def SaveRow(self, model, row, chaves, parent_field, parent_id):
        try:            
            
            id_desktop = row["id_desktop"]
            mod = self.GetModelExistente(chaves=chaves, class_model=model,
                json_registro = row)
       
            for field in row.keys():

                #if field == parent_field:
                #    field_obj = model._meta.get_field(field)    
                #    setattr(mod, self.GetNomeColunaBd(field_obj), row[field])
                #    continue
                                
                if not field in ["model_child"]:
                    
                    field_obj = model._meta.get_field(field)    

                    Valor_fk_ou_padrao = self.GetIdModelPaiOuValorFiltro(field_obj = field_obj, 
                        nome_campo_filtro = "id_desktop", valor_filtro = row[field])                                        

                    setattr(mod, self.GetNomeColunaBd(field_obj), Valor_fk_ou_padrao)

            #setattr(mod, "id_desktop", id_desktop)
            try:
                mod.full_clean()
                mod.save()           
            except Exception as e:
                return str('Erro ao inserir o model:' + model.__name__ + ': ' + str(e))

            self.str_lista_id_desktop += id_desktop + ":" +  str(mod.id) + ";"

            return mod.id

        except Exception as e:
            return str(e)

