from django.shortcuts import render, render_to_response, HttpResponse
from django.contrib.auth.decorators import login_required
import os
import json
from django.contrib.staticfiles.templatetags.staticfiles import static

# Create your views here.
@login_required
def ObterImagens(request):
    diretorio_raiz =  os.path.join(os.path.dirname(os.path.dirname(__file__)), 'vcustom/static')
    diretorio = os.path.join(diretorio_raiz, 'imagens_produtos')
    
    imagens = Imagens(diretorio=diretorio)    
    return HttpResponse(imagens.get_files_like_json())




class Imagens(object):
    def __init__(self, diretorio):
        self.diretorio = diretorio
    
    def get_files_like_json(self):
        files = os.listdir(self.diretorio)
        
        files_dict = {}
        
        for fi in files:            
            files_dict.update({fi.replace('.png', '').replace('.jpeg', ''): static('imagens_produtos/' + fi)})
        
        return json.dumps(files_dict)
            