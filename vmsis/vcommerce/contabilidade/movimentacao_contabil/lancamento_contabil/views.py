# from vlib import view_lib, url_lib
# from django.shortcuts import render
from vlib.view_lib import ViewCreate, StandardFormGrid, ViewUpdate
# from django.core.exceptions import ValidationError
# from django.forms import ModelForm, Form


from contabilidade.movimentacao_contabil.lancamento_contabil.models import LancamentoContabil 
from contabilidade.movimentacao_contabil.lancamento_contabil_detalhe.models import LancamentoContabilPartidas 
    
 # Create your views here.

class FormLancamentoContabil(StandardFormGrid):    

    class Meta:
        model = LancamentoContabil        
    
    def after_insert_grid_row(self, instance):
        #usar este método para rodar alguma rotina após a inserção de cada linha do grid
        #o parâmetro instance é o objeto com os dados inseridos no banco de dados pelo grid
        
        #existem os metodos after_update_grid_row e before_delete_grid_row, ambos com o mesmo funcionamento
        #para que funcione tanto no form de inserção quanto no de edição deve-se passar os parametros 
        #ClassCreate e ClassUpdate na urls

        #a cada linha inserida no grid será inserida outra linha identica        
        novo_lancamento = LancamentoContabilPartidas()
        novo_lancamento.numero_lancamento = instance.numero_lancamento
        novo_lancamento.conta_contabil = instance.conta_contabil         
        novo_lancamento.centro_custo = instance.centro_custo
        novo_lancamento.valor_partida = instance.valor_partida
        novo_lancamento.historico_padrao = instance.historico_padrao
        novo_lancamento.historico_complementar = 'inserido automaticamente'
        novo_lancamento.save()
    
    def before_delete_grid_row(self, instance):    
        print(instance)
        
class ViewLancamentoContabilCreate(ViewCreate):  
    form_class = FormLancamentoContabil

class ViewLancamentoContabilUpdate(ViewUpdate):  
    form_class = FormLancamentoContabil

#class ViewLancamentoContabilUpdate(VieDelete):  
#    form_class = FormLancamentoContabil
