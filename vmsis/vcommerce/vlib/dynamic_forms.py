# coding: utf-8
from django.forms import ModelForm, Form
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext



class Dynamic(object):
    def __init__(self, request, model, template, fields = ()):
        self.model = model
        self.fields = fields
        self.request = request
        self.template = template

    def Form(self):
        class DynamicForm(ModelForm):
            class Meta:
                model = self.model
            
                if self.fields:
                    fields = self.fields
        
        return DynamicForm

    def Response(self):
        form = self.Form()
        form_filtro = form()

        return render_to_response(self.template, {'form' : form_filtro, 'model' : self.model}, 
            context_instance=RequestContext(self.request))

    def Form_as_p(self):
        form = self.Form()
        form_filtro = form()
        return form_filtro.as_p()
        
