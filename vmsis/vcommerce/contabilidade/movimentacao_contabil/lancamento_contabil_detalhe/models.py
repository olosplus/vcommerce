from django.db import models
from contabilidade.movimentacao_contabil.lancamento_contabil.models import LancamentoContabil
from contabilidade.cadastro_contabil.plano_conta.models import PlanoConta
from cadastro.centro_custo.models import CentroCusto
from contabilidade.cadastro_contabil.historico_padrao.models import HistoricoPadrao
from vlib.control.models import Master_empresa

# Create your models here.
class LancamentoContabilPartidas(Master_empresa):
    numero_lancamento = models.ForeignKey(LancamentoContabil)
    conta_contabil = models.ForeignKey(PlanoConta)
    centro_custo = models.ForeignKey(CentroCusto)
    valor_partida = models.FloatField(verbose_name = "Valor")
    historico_padrao = models.ForeignKey(HistoricoPadrao)
    historico_complementar = models.TextField(verbose_name = "Histórico complementar", blank = True,
        null = True)
#todo - vefificar se os valores dos lancamentos filhos batem com o valor lançado no valor_partida
#todo - colocar como detalhe do LancamentoContabil