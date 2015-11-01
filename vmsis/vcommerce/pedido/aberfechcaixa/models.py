from django.db import models
from pedido.cadastro_pedido.caixa.models import Caixa
from cadastro.funcionario.models import Funcionario
from vlib.control.models import ControleSincronizacao

choices_status = (('P', 'Pendente'), ('A', 'Aberto'), ('F', 'Fechado'))
# Create your models here.
class AberFechCaixa(ControleSincronizacao):
    caixa = models.ForeignKey(Caixa, verbose_name="Caixa")
    vrinicial = models.FloatField(verbose_name="Valor inicial")
    vrcorrigido = models.FloatField(verbose_name="Valor conferido")
    vrvenda = models.FloatField(verbose_name="Valor das vendas")
    vrretirada = models.FloatField(verbose_name="Valor das retiradas")
    vrsangria = models.FloatField(verbose_name="Valor das sangrias")
    vrentrada = models.FloatField(verbose_name="Valor das entradas")
    vrdebio = models.FloatField(verbose_name="Valor dos débitos")
    vrcredito = models.FloatField(verbose_name="Valor dos créditos")
    dtmovi = models.DateField(verbose_name="Data do movimento")
    funciconfabertura = models.ForeignKey(Funcionario, 
        verbose_name="Funionário de conferência", blank=True, null=True, 
        related_name="funciconfabertura_funcionario")
    funcipreabertura = models.ForeignKey(Funcionario, 
        verbose_name="Funionário de pré-abertura", blank=True, null=True,
        related_name="funcipreabertura_funcionario")    
    funcifechamento = models.ForeignKey(Funcionario, 
        verbose_name="Funionário de fechamento", blank=True, null=True,
        related_name="funcifechamento_funcionario")        
    status = models.CharField(max_length=1, verbose_name="Status da abertura", 
        choices=choices_status)
