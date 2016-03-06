from django.shortcuts import render
from django import forms
from cadastro.produto.models import Produto
from vlib.view_lib import ViewCreate, ViewUpdate, StandardFormGrid

# Create your views here.

class FormProduto(StandardFormGrid):
    class Meta:
        model = Produto
    
    imgindex =  forms.CharField(label="",widget=forms.TextInput(attrs={'class':'dis-none'}))
    

class CreateProduto(ViewCreate):
    form_class = FormProduto

class UpdateProduto(ViewUpdate):
    form_class = FormProduto