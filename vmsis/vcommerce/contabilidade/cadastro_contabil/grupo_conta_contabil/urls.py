from django.conf.urls import patterns
from vlib.view_lib import CrudView
from contabilidade.cadastro_contabil.grupo_conta_contabil.models import GrupoContaContabil

Crud = CrudView(GrupoContaContabil)
urlpatterns = Crud.AsUrl()