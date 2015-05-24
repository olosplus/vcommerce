from django.db import models
from vlib.control.models import Master_empresa

# Create your models here.
class GrupoContaContabil(Master_empresa):
    codigo = models.CharField(verbose_name = "Código", max_length = 2, unique = True)
    descricao = models.CharField(verbose_name = "Descrição", max_length = 50)
    def __str__(self):
        return "%s - %s" % (self.codigo, self.descricao)