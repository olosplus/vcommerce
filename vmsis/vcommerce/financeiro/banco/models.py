from django.db import models
from vlib.control.models import Master_empresa

# Create your models here.
class Banco(Master_empresa):
	class Meta:
		db_table = "banco"
		verbose_name = "Banco"
		verbose_name_plural = "Bancos"
		ordering = ['cdbanco']

	cdbanco = models.CharField(max_length=30,verbose_name="Código",blank=True)
	nmbanco = models.CharField(max_length=200,verbose_name="Banco")
	cnpjbanco = models.CharField(max_length=16,verbose_name="CNPJ")
	dssite = models.CharField(max_length=50,verbose_name="Site")

	def __str__(self):
		if self.cdbanco:
			return self.cdbanco + ' - ' + self.nmbanco
		else:
			return self.nmbanco