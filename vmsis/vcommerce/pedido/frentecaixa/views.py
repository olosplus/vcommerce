# -*- codaftertf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import json
from vlib.grid import Grid
from pedido.frentecaixa.models import Pedido

# Create your views here.
@login_required
def CarregarPedido(request):
#    grade = Grid()
    return render_to_response('pedido/pedido.html', {})
