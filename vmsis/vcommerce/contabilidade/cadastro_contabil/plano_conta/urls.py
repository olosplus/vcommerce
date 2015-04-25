from django.conf.urls import patterns
from vlib.view_lib import CrudView
from contabilidade.cadastro_contabil.plano_conta.models import PlanoConta

Crud = CrudView(PlanoConta)
urlpatterns = Crud.AsUrl(GridFields = ('Nome', 'natureza', 'grupo_conta_contabil__descricao'))