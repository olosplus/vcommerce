from vlib.view_lib import CrudView
from django.conf.urls import patterns
from cadastro.centro_custo.models import CentroCusto
Crud = CrudView(CentroCusto)
urlpatterns = Crud.AsUrl()