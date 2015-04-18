# coding: utf-8
from django.forms import ModelForm, Form
from django.shortcuts import render_to_response, get_object_or_404

TEMPLATE_NAME = 'simple_base.html'

class Filtro(object):
    def __init__(self, request, model, fields = ()):
        self.model = model
        self.fields = fields
        self.request = request

    def Form:
        class FiltroForm(ModelForm):
            class Meta:
                model = self.model
            
                if self.fields:
                    fields = self.fields
        
        return FiltroForm

    def Response:
        form = self.Form
        form_filtro = fom()

        return render_to_response(TEMPLATE_NAME, {'form' : form_filtro}, context_instance=RequestContext(request))