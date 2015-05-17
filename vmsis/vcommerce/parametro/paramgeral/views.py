# -*- coding: utf-8 -*- 
from django import forms
from django.views.generic.edit import UpdateView
from parametro.paramgeral.models import Paramgeral
from vlib.view_lib import TEMPLATE_UPDATE

class ParamGeral(UpdateView):
    model = Paramgeral
    template_name = TEMPLATE_UPDATE