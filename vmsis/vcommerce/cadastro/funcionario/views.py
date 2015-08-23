 # -*- coding: utf-8 -*-
from django import forms
from vlib.view_lib import ViewCreate, StandardFormGrid, ViewDelete
from cadastro.funcionario.models import Funcionario

class FormFuncionario(StandardFormGrid):
    class Meta:
        model = Funcionario

    senha = forms.CharField(max_length=30, widget=forms.PasswordInput(), label='Senha')
    confsenha = forms.CharField(max_length=30, widget=forms.PasswordInput(), 
       label='Confirma Senha')
    cep = forms.CharField(max_length=9, label="CEP", widget=forms.TextInput(attrs={'class':'cep'}))

class ViewFuncionario(ViewCreate):
    form_class = FormFuncionario