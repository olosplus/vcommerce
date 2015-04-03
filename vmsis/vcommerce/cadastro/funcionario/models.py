# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from cadastro.unidade.models import Unidade
from cadastro.empresa.models import Empresa

TIPO_C = (('PF',u'Pessoa Física'),('PJ',u'Pessoa Jurídica'),)
SEXO_C = (('F','Feminino'),('M','Masculino'),)

# Create your models here.
class Funcionario(models.Model):
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
	cep = models.CharField(max_length=9,verbose_name='CEP')
	bairro = models.CharField(max_length=255, blank=True, null=True, verbose_name='Bairro')
	estado = models.CharField(max_length=2,verbose_name='Estado')
	cidade = models.CharField(max_length=255,verbose_name='Cidade')
	dtcadastro = models.DateField(auto_now_add=True, verbose_name='Data de cadastro')
	dtadmissao = models.DateField(verbose_name='Data de admissão',null=True,blank=True)
	dtdemissao = models.DateField(verbose_name='Data de demissão',null=True,blank=True)
	pessoa = models.CharField(max_length=2,verbose_name='Tipo',choices=TIPO_C, blank=True, null=True)
	unidade = models.ForeignKey(Unidade,verbose_name="Unidade", null=True, blank=True)
	#esse unidade aqui em cima seria a default
	'''
    se for olhar a estrutura, tudo que é cadastro praticamente todos são por empresa, ou seja, outras unidades
    poderiam ter acesso... já os sistemas estoque por exemplo ou contabil, teria que ser por unidade, dai 
    conseguiriamos filtrar tanto pela empresa toda ou pela unidade, tendeu?
    não..kkkk.Vai ter empresa em todos os cadastros e unidade em alguns sistemas?
    isso, nos cadastros terão empresa porque todas as unidades de determinada empresa vao compartilhar
    as mesmas informações de cliente, fornecedor, produtos... etc

    então só as movimentações teriam a unidade..

    sim, poruqe da movimentação consigo chegar na empresa, e caso seja necessario filtrar apenas movimentações
    de determinada unidade iriamos conseguir

    entendi, olha colocar isso na classe pai não é complicado, na verdade é aquilo que vc me viu fazer,
    mas vamos ter que implemetar primeiro a rotina do usuario logar na empresa e escolher a unidade que ele possui
    acesso...daí criariamos o metodo para obter a instancia da unidade e salvar no formulario...

    como faria para no caso do funcionario, tipo no cadastro dele eu iria salvar a empresa que eu estivesse logado
    mas o primeiro usuario do sistema a gente que teria q cadastrar e se fizermos (coisa que nao consegui direito)
    fazer pegar a empresa do usuario que está logado cadastrando o funcionario (pera que me embolei kkkk)
    resumindo, acha q o primeiro usuario podemos cadastrar pelo banco? kkkk


   si sim
ras
    então acho que da pra fazer assim, 
    tipo o usuario o proprio django pode cadastrar, só iria faltar os funcionarios...
    tipo poderiamos criar um usuario admin quando formos criar o syncdb da empresa, 
    daí criariamos as unidades e funcionarios e outros usuarios com esse usuario...não 
    dá pra fazer assim?

    mais ou menos, tipo pq o campo de escolher a empresa do funcionario que esta sendo cadastrado queria deixar 
    oculto, dai a gente cadastrando apenas o primeiro funcionario que seria o principal para a empresa, 
    precisariamos cadastrar apenas um almoxarifado qualquer (ou já deixar um previamente inserido) o mesmo 
    acontecendo com a empresa que teriamos que cadastrar. dai o resto o empreendedor se virava

    não entendi a parte da empresa oculta...a empresa fica na tabela de funcionário ou usuario?

    funcionario, dai eu iria inserir sempre a empresa de quem estivesse cadastrando o carinha hehe
    mas, tipo como definiria a empresa dos funcionarios..tipo a primeira seria inserida pelo banco,
    mas se o gerente quiser cadastrar um funcionário para outra empresa que não seja a que cadastramos
    primeiro, teriamos que inserir no bnaco para ele?

    ai que tá, na minha cabeça cada licensa de uso seria para uma empresa, e caso a empresa tenha varias
    unidades iria cadastrar elas, todos pra msm empresa (que estivesse logado), tipo os dados de cnpj etc
    eu coloquei um na tabela de empresa bem no cadastro... mas ela insere sozinha uma unidade "matriz"

    saquei, então toda vez que o cliente quissese colocar outra empresa ele teria que entar em contato
    para nós controlarmos a licensa e cadastrariamos um empresa e outro usuario master para aquela empresa?

    sim, ou uma outra opção é ele cadastrar uma unidade, que nada mais é do que uma empresa... tem todas 
    informações de uma empresa

    saquei, a unidade é como se fosse uma filial então
    ...
    sim, pode ter cnpj e tudo mais

    blz..o que vc quer fazer primeiro, oq vc já fez?

    nao fiz muita coisa, fiquei maior parte do tempo tentando imaginar como iria fazer isso... a principio
    joguei a empresa em todos os models menos os de localidade, já que fiquei em duvida se iria manter um 
    cadastro de bairro, cidade etc.. para todos as empresas (isso em comum) só que o ruim disso se alguem
    chegar e cadastrar lactose como pais, todas outras empresas iriam ver
    dai eu nao sabia como colocar a empresa pra ser inserida, porque nao sabia que dava pra mexer direto la,
    ou mexer extendendo a view igual vc me mostrou

    isso aí vc  não precisa mexer pq coloco na classe paisna vlib..eu criei um form padrão lá que vamos herdar
    caso precisemos fazer alguma validação extra....só preciso dar uma organizada lá pq fiz uma zona mexendo no grid
    kkkk

    kkkk aqui,entao de inicio teriamos que tratar de arrumar para a empresa ser adicionada nas tabelas e depois
    partir pra unidade?

    sim, então o relacionamento seria o funcionario com a empresa....tipo, eu consigo pegar o funcionario a partir
    do user do django?

    sim, tirando o primeiro usuario que é criado no syncdb, os outros que cadastrarmos no model funcionario vai 
    direto inserindo um user, olha ai em baixo
 com o user criado pelo django vai dar pra inserir o funcionario?
 do jeito que tá agora sim, porque consigo escolher a empresa... o campo empresa aparece no browser, 
 queria deixar oculto e inserir sempre a empresa do outro funcionario que ta cadastrando o funcionario kkkk


 da pra fazer um tratameto pra ver se a tabela funcionário está vazia, se estiver mostra a empresa, se não,
 esconde a empresa...não acha melhor? Aí dá pra fazer o cdastro pela tela mesmo e aí o usuário não iria conseguir

 acho que seria sim, seria bem melhor... soh que precisaremos apenas filtrar por empresa hehe senao caso jah
 tenha uma empresa funcionando nao iriamos conseguir cadastrar um funcionario inicial para outra empresa

 hum, o cadastro de empresa não vai existir no sistema?
 pra gente vai, mas nenhum usuario vai ver hehe vou jogar visible dela pra False

 hum, saquei, então dá pra fazer o filtro no cadastro do funcionário, pq de qualquer forma o cliente não
 consegue cadastrar empresa por si só..teria que entrar em contato e pagar ehehe...desde que nós façamos o 
 cadastro de empresa o resto tá fechado....

 isso, me manda aquela parte que vc mexeu ai, na view_lib se nao me engano, pra identificar se eh empresa ou 
 unidade e gravar... to morrendo de sono kkkk

 kkk...foi no form, mas vc não tem o form na sua vlib, vou ter que te mandar ela toda...deixa eu só mudar 
 uma parada nela para permitir sobrescrita se não depois vai ficar ruim de mudar, pq teriamos que refazer..
 vc vai trabalhar amanhâ?
 vou e vc?

 não..vou mexer nessa parte e te mandar então
 pera entao, me manda a sua do jeito que ta ai... pq mexi em algumas coisas dai tenho que atualizar o seu com 
 oq mexi sem sobrescrever oq vc fez, dai ti mando

 vou te mandar no E-mail

 ok, aqui depois coloca os cadastros que vc precisar aqui no meio tambem, pra deixar todos juntos... depois vemos
 como iriamos deixar alguns invisiveis caso o cliente nao tivesse "tais" modulos
 pq dai ti mando o virtualenv inteiro hehe

 blz

 vou te mandar o projeto todo...

 ta

 vou sair aqui...deixar vc dormir...te mando o projeto agora aí..

 ta, pq dai altero e ti mando e vou dormir kkkk

 kkkkflw

 flws

 





	'''
	empresa = models.ForeignKey(Empresa,verbose_name="Empresa", null=True)

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