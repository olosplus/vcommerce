from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView
from contabilidade.parametro.parametro_contabilidade.model import  ParametroContabilidade

Crud = CrudView(ParametroContabilidade)
urlpatterns = Crud.AsUrl()