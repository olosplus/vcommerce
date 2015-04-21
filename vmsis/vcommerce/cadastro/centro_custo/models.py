# coding : utf-8
from django.db import models

# Create your models here.
class CentroCusto(models.Model):
    codigo = models.IntegerField(verbose_name = "Código", unique = True)
    nome = models.CharField(verbose_name = "Nome", unique = True, max_length = 100)

    def __str__(self):
        return "%s - %s" % (self.codigo, self.nome)


