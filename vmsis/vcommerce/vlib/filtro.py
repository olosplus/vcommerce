# coding: utf-8
from django.forms import ModelForm, Form
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


TEMPLATE_NAME = 'simple_base.html'

class Filtro(object):
    def __init__(self, request, model, fields = ()):
        self.model = model
        self.fields = fields
        self.request = request

    def Form(self):
        class FiltroForm(ModelForm):
            class Meta:
                model = self.model
            
                if self.fields:
                    fields = self.fields
        
        return FiltroForm

    def Response(self):
        form = self.Form()
        form_filtro = form()

        return render_to_response(TEMPLATE_NAME, {'form' : form_filtro, 'model' : self.model}, 
            context_instance=RequestContext(self.request))

    def Form_as_p(self):
        form = self.Form()
        form_filtro = form()
        return form_filtro.as_p()
        
