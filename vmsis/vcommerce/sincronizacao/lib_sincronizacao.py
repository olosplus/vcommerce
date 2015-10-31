import json
from django.core.exceptions import ValidationError
from django.core import serializers
from django.http import HttpResponse
from django.db import models
from vlib.libs import lib_auxiliar
from django.db import IntegrityError

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
    def __init__(self, usuario, senha, model):
        super(DownloadModel, self).__init__(usuario, senha)
        self.fields = []
        self.filtro = {}
        self.model = model
            
    def GetDataAsXML(self):
        if not self.Autenticado():
            return HttpResponse('Login error')

        if self.filtro:
            condicao = json.loads(self.filtro)
            objs = self.model.objects.filter(**condicao)
        else:
            objs = self.model.objects.all()
        
        try:
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
    

    def SaveRow(self, model, row, chaves, parent_field, parent_id):
        try:            
            desktop_id = str()            
            mod = None
            
            if chaves:
                lista_chaves = chaves.split(',')
                for chave in lista_chaves:
                    if chave == str():
                        continue

                    try:
                        filtro_chave = {chave : row[chave]}                        
                        mod = model.objects.get(**filtro_chave)
                        if mod:
                            break
                    except model.DoesNotExist:
                        mod = None  
                        
            if not mod:
                mod = model()
            
            for field in row.keys():
                if not field in ["model_child", "desktop_id"]:
                    setattr(mod, field, row[field])
                else: 
                    if field == "desktop_id":
                        desktop_id = row[field]

            if parent_id:
                setattr(mod, parent_field, parent_id)

            mod.save()
            
            self.str_lista_id_desktop += desktop_id + ":" +  str(mod.id) + ";"

            return mod.id

        except Exception as e:
            print(e)
            return str(e)

    def SaveJson(self, json_data, parent_id):
        if not self.Autenticado():
           return HttpResponse('Error|Login error')
        
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
            
            id = self.SaveRow(model = model, row = row, chaves = chaves, 
                parent_field = parent_field, parent_id = parent_id)

            #retorna mensagem de erro caso não haja sucesso
            if type(id) == str:
                return HttpResponse("Error|" + id)
            
            if "model_child" in row.keys():
                for child in row["model_child"]:
                    self.SaveJson(child, id)
            
        return HttpResponse("success|" + self.str_lista_id_desktop)
