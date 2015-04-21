# coding: utf-8
from django.db import models

# Create your models here.
class TipoEscrituracaoContabil(models.Model):
    tipo = models.CharField(verbose_name = "Tipo", max_length = 1)
    descricao = models.CharField(verbose_name = "Descrição", max_length = 100)
    def __str__(self):
        return self.descricao