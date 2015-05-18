 # -*- coding: utf-8 -*-
from django import forms
from vlib.view_lib import ViewCreate, StandardFormGrid, ViewDelete
from cadastro.funcionario.models import Funcionario

class FormFuncionario(StandardFormGrid):
    class Meta:
        model = Funcionario
    senha = forms.CharField(max_length=30, widget=forms.PasswordInput())

class ViewFuncionario(ViewCreate):
    form_class = FormFuncionario