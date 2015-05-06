# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from cadastro.unidade.models import Unidade
from vlib.control.models import Master_empresa
from cadastro.localidade.bairro.models import Bairro
from cadastro.localidade.cidade.models import Cidade
from cadastro.localidade.estado.models import Estado

TIPO_C = (('PF',u'Pessoa Física'),('PJ',u'Pessoa Jurídica'),)
SEXO_C = (('F','Feminino'),('M','Masculino'),)

# Create your models here.
class Funcionario(Master_empresa):
	user = models.ForeignKey(User, blank=True, null=True, editable=False)

	nome = models.CharField(max_length=255, verbose_name='Nome')
	usuario = models.CharField(max_length=255, verbose_name='Usuário')
	sexo = models.CharField(max_length=1,choices=SEXO_C, verbose_name='Sexo')
	dtnascimento = models.DateField(verbose_name='Data de nascimento',null=True,blank=True)
	email = models.EmailField(max_length=255, verbose_name='E-mail')
	senha = models.CharField(max_length=30, verbose_name='Senha')
	endereco = models.CharField(max_length=255, verbose_name='Endereço', blank=True, null=True)
	numero = models.CharField(max_length=20, verbose_name='Número', blank=True, null=True)
	complemento = models.CharField(max_length=255, null=True, blank=True, verbose_name='Complemento')
	cep = models.CharField(max_length=9,verbose_name='CEP', null=True)
	bairro = models.ForeignKey(Bairro, blank=True, null=True, verbose_name='Bairro')
	cidade = models.ForeignKey(Cidade,verbose_name='Cidade', null=True)
	estado = models.ForeignKey(Estado,verbose_name='Estado', null=True)
	dtcadastro = models.DateField(auto_now_add=True, verbose_name='Data de cadastro')
	dtadmissao = models.DateField(verbose_name='Data de admissão',null=True,blank=True)
	dtdemissao = models.DateField(verbose_name='Data de demissão',null=True,blank=True)
	pessoa = models.CharField(max_length=2,verbose_name='Tipo',choices=TIPO_C, blank=True, null=True)
#	unidadePadrao = models.CharField(verbose_name="Unidade padrão", QuerySet=Unidade.objects.all())
	unidade = models.ManyToManyField(Unidade, verbose_name="Unidades permitidas", blank=True, null=True)

	class Meta:
		ordering = ['-id']

	def save(self):
		if not self.id:
			c = Funcionario.objects.filter(usuario=self.usuario).count()
			if c:
				raise UsuarioExistente
			usr = User.objects.filter(username=self.usuario)
			if usr:
				u = usr[0]
			else:
				u = User.objects.create_user(self.usuario, self.email, self.senha)
			u.save()
			self.user = u
		else:
			self.user.username = self.usuario
			self.user.email = self.email
			self.user.set_password(self.senha)
			self.user.save()

		super(Funcionario, self).save()

		def __str__(self):
		    return self.nome