# -*- coding: utf-8 -*-
from django.db import models
from cadastro.empresa.models import Empresa

choice_marcado = (('S','Sim'),
	('N','Não'))

# Create your models here.
class Personaliza(models.Model):
	class Meta:
		db_table = "personaliza"
		verbose_name = "Personalização"
		verbose_name_plural = "Personalizações"

	empresa = models.ForeignKey(Empresa,verbose_name="Empresa")
	logo_pic = models.ImageField(upload_to='logos')
    #idutilinve = models.CharField(max_length=1,verbose_name="Utiliza inventário",choices=choice_marcado)	
	#logo_pic = models.ImageField(upload_to = 'logo_folder/', default = 'logo_folder/None/vmsis.jpg')