from django.conf.urls import patterns
from vlib.view_lib import CrudView
from contabilidade.cadastro_contabil.tipo_escrituracao.models import TipoEscrituracaoContabil

Crud = CrudView(TipoEscrituracaoContabil)
urlpatterns = Crud.AsUrl()
