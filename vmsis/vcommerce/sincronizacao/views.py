from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core import serializers
from vlib.libs import lib_auxiliar
from sincronizacao import lib_sincronizacao as lib_sinc
import json
import datetime


#views method
def GetModelAsXML(request):
    try:
        senha = request.GET.get('senha')
        usuario = request.GET.get('usuario')
    except Exception:
        return HttpResponse('Login error')
    
    str_model = request.GET.get('model')
    str_module = request.GET.get('module')
    fields = request.GET.get('fields', [])
    filtro = request.GET.get('filter', {})
    DataUltimaSinc = request.GET.get('DataInicial', datetime.datetime.now())
    
    if fields:
        fields = fields.split("|")    
    
    try:
        model = lib_auxiliar.get_model_by_string(str_module, str_model)
    except LookupError:
        return HttpResponse("An error ocurred. The model or module don't exists")
       
    sinc = lib_sinc.DownloadModel(usuario, senha, model, DataUltimaSinc)
    sinc.fields = fields
    sinc.filtro = filtro
    return sinc.GetDataAsXML()

@csrf_exempt
def SaveJsonAsModel(request):
    #try:
    #    senha = request.POST['senha']
    #    usuario = request.POST['usuario']
    #except Exception:
    #    return HttpResponse('Error|Login error')
    senha = 'masterVMSIS123v'
    usuario = 'vmsismaster'
    try:
        data_str = request.POST['data']
    
        data_dict = {}
    
        if data_str:
            data_dict = dict(json.loads(data_str))
    except Exception as e:
        return HttpResponse('Error|' + str(e) )
    
    upload = lib_sinc.UploadModel(usuario, senha)
    return upload.SaveJson(data_dict, parent_id = None)
