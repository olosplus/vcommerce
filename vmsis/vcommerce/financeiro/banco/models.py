from django.db import models

# Create your models here.
class Banco(models.Model):
	class Meta:
		db_table = "banco"
		verbose_name = "Banco"
		verbose_name_plural = "Bancos"

	cdbanco = models.CharField(max_length=30,verbose_name="Codigo",blank=True)
	nmbanco = models.CharField(max_length=200,verbose_name="Banco")
	cnpjbanco = models.CharField(max_length=16,verbose_name="CNPJ")

	def __str__(self):
		return self.nmbanco