from django.db import models
from cadastro.empresa.models import Empresa

from contabilidade.cadastro_contabil.plano_conta.models import PlanoConta
from cadastro.centro_custo.models import CentroCusto
from contabilidade.cadastro_contabil.historico_padrao.models import HistoricoPadrao

# Create your models here.
class LancamentoContabil(models.Model):
    class Meta:
        child_models = ['contabilidade.movimentacao_contabil.lancamento_contabil_detalhe.'+
            'models.LancamentoContabilPartidas']

    empresa = models.ForeignKey(Empresa)
    numero_lancamento = models.IntegerField(verbose_name = "Número do lançamento")
    data_lancamento = models.DateField(verbose_name = "Data do lançamento")
    valor = models.FloatField(verbose_name = "Valor")

    def __str__(self):
        return "%s - %s - %s" % (self.empresa, self.numero_lancamento, self.valor)
        
#class LancamentoContabilPartidas(models.Model):
#    numero_lancamento = models.ForeignKey(LancamentoContabil)
#    conta_contabil = models.ForeignKey(PlanoConta)
#    centro_custo = models.ForeignKey(CentroCusto)
#    valor_partida = models.FloatField(verbose_name = "Valor")
#    historico_padrao = models.ForeignKey(HistoricoPadrao)
#    historico_complementar = models.TextField(verbose_name = "Histórico complementar", blank = True,
#        null = True)
#todo - vefificar se os valores dos lancamentos filhos batem com o valor lançado no valor_partida
#todo - colocar como detalhe do LancamentoContabil    