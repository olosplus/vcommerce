from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from cadastro.cliente.models import Cliente

from control.ext_views import ProtectedView

class ClienteInsert(ProtectedView, CreateView):
    model = Cliente
    template_name = 'insert_form.html'
    success_url = '/'

class ClienteDelete(ProtectedView, DeleteView):
    model = Cliente
    template_name = 'remove_form.html'
    success_url = '/'

class ClienteUpdate(ProtectedView, UpdateView):
    model = Cliente
    template_name = 'update_form.html'
    success_url = '/'

class ClienteList(ProtectedView, ListView):
    model = Cliente
    template_name = 'list_form.html'
    def get_context_data(self, **kwargs):
        context = super(ClienteList, self).get_context_data(**kwargs)
        context['titulo'] = 'Clientes'
        return context