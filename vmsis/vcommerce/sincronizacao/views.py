from django.http import HttpResponse

from django.core.exceptions import ValidationError
from django.core import serializers
from vlib.libs import lib_auxiliar
from sincronizacao import lib_sincronizacao as lib_sinc
import json

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
    
    if fields:
        fields = fields.split("|")    
    
    try:
        model = lib_auxiliar.get_model_by_string(str_module, str_model)
    except LookupError:
        return HttpResponse("An error ocurred. The model or module don't exists")
       
    sinc = lib_sinc.DownloadModel(usuario, senha, model)
    sinc.fields = fields
    sinc.filtro = filtro
    return sinc.GetDataAsXML()


def SaveJsonAsModel(request):
    try:
        senha = request.GET.get('senha')
        usuario = request.GET.get('usuario')
    except Exception:
        return HttpResponse('Login error')

    data_str = request.GET.get('data', "")
    
    data_dict = {}

    if data_str:
        data_dict = dict(json.loads(data_str))

    upload = lib_sinc.UploadModel(usuario, senha)

    return upload.SaveJson(data_dict, parent_id = None)
