from django.db import models
from contabilidade.movimentacao_contabil.lancamento_contabil.models import LancamentoContabil
from contabilidade.cadastro_contabil.plano_conta.models import PlanoConta
from cadastro.centro_custo.models import CentroCusto
from contabilidade.cadastro_contabil.historico_padrao.models import HistoricoPadrao
from vlib.control.models import Master_empresa

# Create your models here.

natureza = (('D', 'Débito'), ('C', 'Crédito'))

class LancamentoContabilPartidas(Master_empresa):
    class Meta:
        verbose_name = "Lançamentos detalhados"

    numero_lancamento = models.ForeignKey(LancamentoContabil)
    conta_contabil = models.ForeignKey(PlanoConta, verbose_name="Conta contábil")
    centro_custo = models.ForeignKey(CentroCusto, verbose_name="Centro de custo")
    valor_partida = models.FloatField(verbose_name = "Valor")
    historico_padrao = models.ForeignKey(HistoricoPadrao, verbose_name="Histórico padrão")
    historico_complementar = models.TextField(verbose_name = "Histórico complementar", blank = True,
        null = True)
    natureza = models.CharField(max_length=1, verbose_name="Tipo da operação", choices=natureza)

#todo - vefificar se os valores dos lancamentos filhos batem com o valor lançado no valor_partida
#todo - colocar como detalhe do LancamentoContabil