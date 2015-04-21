# from vlib import view_lib, url_lib
# from django.shortcuts import render
# from vlib.view_lib import ViewCreate, StandardFormGrid
# from django.core.exceptions import ValidationError
# from django.forms import ModelForm, Form


# from contabilidade.movimentacao_contabil.lancamento_contabil.models import LancamentoContabil, LancamentoContabilPartidas
# # Create your views here.

# class FormLancamentoContabil(StandardFormGrid):    

#     class Meta:
#         model = LancamentoContabil        
        
    
#     def save(self, commit = False):
#         instance = super(FormLancamentoContabil, self).save(commit=True)

#         lanc = LancamentoContabilPartidas()
#         setattr(lanc, 'numero_lancamento' , instance)
#         setattr(lanc, 'valor_partida' , instance.valor)        
        
#         try:
#             lanc.full_clean()
#         except ValidationError as e:
#             raise
#         else:
#             lanc.save() 

# class ViewLancamentoContabil(view_lib.ViewCreate):  

# #    FormLancamentoContabil.Meta.model = model
#     form_class = FormLancamentoContabil
