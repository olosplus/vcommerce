from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect

#from django.views.generic import TemplateView
#from django.views.generic.edit import CreateView, UpdateView, DeleteView
#from django.views.generic.list import ListView
from cadastro.cliente.models import Cliente

from vlib.view_lib import ViewCreate, StandardFormGrid, ViewDelete

