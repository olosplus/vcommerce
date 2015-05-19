from vlib.view_lib import CrudView
from django.conf.urls import patterns
from contabilidade.movimentacao_contabil.lancamento_contabil.models import LancamentoContabil
from contabilidade.movimentacao_contabil.lancamento_contabil.views import ViewLancamentoContabilCreate, \
    ViewLancamentoContabilUpdate

Crud = CrudView(LancamentoContabil)
urlpatterns = Crud.AsUrl(ClassCreate = ViewLancamentoContabilCreate, ClassUpdate = ViewLancamentoContabilUpdate)