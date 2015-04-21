# coding: utf-8
from django.db import models
from contabilidade.cadastro_contabil.grupo_conta_contabil.models import GrupoContaContabil
import datetime
from django.core.exceptions import ValidationError

tipos_contas = (('A', 'Analítica'), ('S', 'Sintética') )
naturezas = (('D', 'Devedora'), ('C', 'Credora'))

# Create your models here.
class PlanoConta(models.Model):
    codigo = models.CharField(verbose_name = "Código", max_length = 20, unique = True)
    Nome = models.CharField(verbose_name = "Descrição", max_length = 300)
    tipo_conta = models.CharField(verbose_name = "Tipo", choices = tipos_contas, max_length = 1)
    nivel = models.IntegerField()
    grupo_conta_contabil = models.ForeignKey(GrupoContaContabil)
    natureza = models.CharField(verbose_name = "Natureza", max_length = 1, choices = naturezas)
    data_inclusao = models.DateField(default = datetime.date.today(), editable = False)
    data_ultima_alteracao = models.DateField(null = True, blank = True, editable = False)

    def Clean(self):

        if self.data_inclusao != self.data_ultima_alteracao:
            self.data_ultima_alteracao = datetime.date.today()

        if self.nivel <= 0 :
            raise ValidationError("O campo nível só aceita valores maiores do que (0)zero")
            