from django.db import models
from pedido.frentecaixa.models import Pedido
from pedido.cadastro_pedido.caixa.models import Caixa

tipo_movimento = (('E', 'Entrada'), ('V', 'Venda'), ('S', 'Sangria'), ('R', 'Retirada'))
forma_pagamento = (('DI', 'Dinheiro'), ('DE', 'Débito'), ('CR', 'Crédito'))

# Create your models here.
class MovCaixa(models.Model):
    caixa = models.ForeignKey(Caixa, verbose_name="Caixa")
    dtmovi = models.DateField(verbose_name="Data do lancamento")
    vrmovi = models.FloatField(verbose_name="Valor do pedido")
    tpmovi = models.CharField(max_length=1, verbose_name="Tipo do movimento", 
        choices=tipo_movimento)
    formpgto = models.CharField(max_length=1, verbose_name="Forma de pagamento",
        choices=forma_pagamento)
    pedido = models.ForeignKey(Pedido, verbose_name="Pedido", null=True, blank=True)

    class Meta:
        db_table = "MovCaixa"
        verbose_name = "Movimentação do caixa"

