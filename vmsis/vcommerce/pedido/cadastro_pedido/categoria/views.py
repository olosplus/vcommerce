from django.shortcuts import render
from django import forms
from pedido.cadastro_pedido.categoria.models import Categoria
from vlib.view_lib import ViewCreate, ViewUpdate, StandardFormGrid

# Create your views here.

class FormCategoria(StandardFormGrid):
    class Meta:
        model = Categoria
    
    imgindex =  forms.CharField(label="",widget=forms.TextInput(attrs={'class':'dis-none'}))
    

class CreateCategoria(ViewCreate):
    form_class = FormCategoria

class UpdateCategoria(ViewUpdate):
    form_class = FormCategoria