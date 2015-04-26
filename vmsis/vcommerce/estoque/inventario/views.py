from vlib.view_lib import ViewCreate, StandardFormGrid  
from estoque.inventario.models import Inventario
from estoque.posestoque.models import Posestoque
from estoque.itemproduto.models import Itemproduto
    
# Create your views here.

class FormInventario(StandardFormGrid):
    class Meta:
        model = Inventario
    
    def after_insert_grid_row(self, instance):  
        novo_lancamento = Posestoque()
        novo_lancamento.movimentacaoest = instance.id
        novo_lancamento.produto = instance.produto
        novo_lancamento.almoxarifado = instance.almoxarifado        
        #novo_lancamento.lote = instance.lote
        novo_lancamento.qtdeproduto = instance.qtdeprod
        novo_lancamento.save()
    
class ViewInventario(ViewCreate):
    form_class = FormInventario