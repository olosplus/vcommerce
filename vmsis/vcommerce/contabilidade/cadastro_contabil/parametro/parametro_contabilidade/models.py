from django.db import models
from contabilidade.cadastro_contabil.tipo_escrituracao.models import TipoEscrituracao
# Create your models here.
class ParametroContabilidade(models.Model):
    tipo_escrituracao = models.ForeignKey(TipoEscrituracao)