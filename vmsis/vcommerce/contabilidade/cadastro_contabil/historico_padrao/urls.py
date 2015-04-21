from django.conf.urls import patterns
from vlib.view_lib import CrudView
from contabilidade.cadastro_contabil.historico_padrao.models import HistoricoPadrao

Crud = CrudView(HistoricoPadrao)
urlpatterns = Crud.AsUrl()