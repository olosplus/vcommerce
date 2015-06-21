from django.db import models
from pedido.frentecaixa.models import Pedido, ItemPedido
from cadastro.produto.models import Produto
from cadastro.almoxarifado.models import Almoxarifado
from estoque.lote.models import Lote


# Create your models here.
class ItemReti(models.Model):
    class Meta:
        db_table = "itemreti"
        verbose_name = "Ajuste Pedido"
        verbose_name_plural = "Ajustes Pedidos"
        #child_models = ['ItemPedido']
    pedido = models.ForeignKey(Pedido, verbose_name="Pedido")
    item = models.ForeignKey(Produto, verbose_name="Produto")
    almoxarifado = models.ForeignKey(Almoxarifado,verbose_name='Almoxarifado', editable=False)
    lote = models.ForeignKey(Lote,verbose_name='Lote', null=True, blank=True)
    qtreti = models.FloatField(verbose_name="Quantidade")
