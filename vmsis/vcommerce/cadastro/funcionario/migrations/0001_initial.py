# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('usuario', models.CharField(max_length=255, verbose_name='Usuário')),
                ('sexo', models.CharField(max_length=1, choices=[('F', 'Feminino'), ('M', 'Masculino')], verbose_name='Sexo')),
                ('dtnascimento', models.DateField(blank=True, null=True, verbose_name='Data de nascimento')),
                ('email', models.EmailField(max_length=255, verbose_name='E-mail')),
                ('senha', models.CharField(max_length=30, verbose_name='Senha')),
                ('endereco', models.CharField(max_length=255, blank=True, null=True, verbose_name='Endereço')),
                ('numero', models.CharField(max_length=20, blank=True, null=True, verbose_name='Número')),
                ('complemento', models.CharField(max_length=255, blank=True, null=True, verbose_name='Complemento')),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('bairro', models.CharField(max_length=255, blank=True, null=True, verbose_name='Bairro')),
                ('estado', models.CharField(max_length=2, verbose_name='Estado')),
                ('cidade', models.CharField(max_length=255, verbose_name='Cidade')),
                ('dtadmissao', models.DateField(blank=True, null=True, verbose_name='Data de admissão')),
                ('dtdemissao', models.DateField(blank=True, null=True, verbose_name='Data de demissão')),
                ('pessoa', models.CharField(max_length=2, null=True, verbose_name='Tipo', choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, editable=False, null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
    ]
