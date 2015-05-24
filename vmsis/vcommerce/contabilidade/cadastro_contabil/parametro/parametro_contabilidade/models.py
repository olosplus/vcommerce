from django.db import models
from vlib.control.models import Master_empresa
from contabilidade.cadastro_contabil.tipo_escrituracao.models import TipoEscrituracao

# Create your models here.
class ParametroContabilidade(Master_empresa):
    tipo_escrituracao = models.ForeignKey(TipoEscrituracao)