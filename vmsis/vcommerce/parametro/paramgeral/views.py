# -*- coding: utf-8 -*- 
from django import forms
from django.views.generic.edit import UpdateView
from parametro.paramgeral.models import Paramgeral
from vlib.view_lib import TEMPLATE_UPDATE, ViewUpdate

class ParamGeralView(ViewUpdate):
    model = Paramgeral
    template_name = TEMPLATE_UPDATE

    def get_context_data(self, **kwargs): 
        context = super(ParamGeralView, self).get_context_data(**kwargs)
        empresa = self.request.session['funcionario']['empresa']
        if empresa:
            context['object'] = Paramgeral.objects.get(pk=empresa)
        return context