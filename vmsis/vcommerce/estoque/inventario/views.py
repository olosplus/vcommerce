from vlib.view_lib import ViewCreate, StandardFormGrid  
from estoque.inventario.models import Inventario
from estoque.posestoque.models import Posestoque
from estoque.itemproduto.models import Itemproduto
from estoque.lib_est.estoque import Estoque
    
# Create your views here.

class FormInventario(StandardFormGrid):
    class Meta:
        model = Inventario
    
    def after_insert_grid_row(self, instance):
        FunEstoque = Estoque(self.funcionario["empresa"])
        FunEstoque.entr_prod_est(instance.produto_id, instance.almoxarifado, None, instance.qtdeprod)
        print(FunEstoque.qtde_prod_est(instance.produto_id, instance.almoxarifado, None))

class ViewInventario(ViewCreate):
    form_class = FormInventario