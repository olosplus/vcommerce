from vlib.view_lib import ViewCreate, StandardFormGrid  
from estoque.entrada.models import Entrada
from estoque.itemproduto.models import Itemproduto
from estoque.lib_est.estoque import Estoque

class FormEntrada(StandardFormGrid):
    class Meta:
        model = Entrada
    
    def after_insert_grid_row(self, instance):
        FunEstoque = Estoque(self.funcionario["empresa"])
        if FunEstoque.entr_prod_est(instance.produto_id, instance.almoxarifado, instance.lote_id, instance.qtdeprod):
        	Entrada.objects.get(pk=instance.master_moviest_id).delete()

class ViewEntrada(ViewCreate):
    form_class = FormEntrada