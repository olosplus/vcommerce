# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from vlib.vReport.vReport import MasterBand, PageFooter, PageHeader, Report, GroupHeader
from pedido.cadastro_pedido.itemcategoria.models import ItemCategoria, ItAgrupAdicional
from pedido.cadastro_pedido.agrupadicional.models import Adicionais
from cadastro.produto.models import Produto
from django.contrib.auth.decorators import login_required
from django.db import connection
# Create your views here.

class CardapioRel():
    def dictfetchall(self, cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
    
    def get_header(self):
        header = PageHeader()        
        style_label_header = 'font-family: "Times New Roman", Times, serif; font-style: normal;font-size: 20px; '\
            'font-weight: bold;margin:13px auto;width:100%; text-align:center';
        header.set_style(style = "border-bottom:solid 1px black;background-color:silver" )            
        header.add_component(type = "p", name = "lblTitulo", text = "Cardápio / Agrupamentos", 
            style = style_label_header)            
        header.add_component(type = "p", name = "lblLinhaHeader", text = "", 
            style = "border-bottom:solid 1px black;float:left;width:100%")        
        header.add_component(type="div", name="cardapio", text= "Cardápio " , 
            style="margin:3px 5px 3px 1px; float:left; width:100%; font-weight:bold;")
        header.add_component(type="div", name="agrupamento", text= "Agrupamentos " , 
            style="margin:3px 5px 3px 23px; float:left; width:100%; font-weight:bold;")
        header.add_component(type="div", name="adicional", text= "Adicionais " ,    
            style="margin:3px 5px 3px 43px; float:left; width:100%; font-weight:bold;")        
        return header

    def get_group_header_cardapio(self):
        group_header_cardapio = GroupHeader('id_adic')
        group_header_cardapio.set_style('background-color:silver')        
        group_header_cardapio.add_component(type="dataP", name="cardapio__dsproduto", db_link="cardapio__dsproduto",
                                   style="margin:3px 5px 3px 1px;float:left;width:50%;font-wight:bold;font-size:20px;")
        return group_header_cardapio
    
    def get_group_header_agrupadicional(self):
        group_header_agrupadicional= GroupHeader('id_agra')       
        group_header_agrupadicional.add_component(type="dataP", name="agrupadicional__nmagrupadic", db_link="agrupadicional__nmagrupadic",
                                   style="margin:3px 5px 3px 23px;float:left;width:50%;font-wight:bold;font-size:20px;")        
        return group_header_agrupadicional
    
    def get_master_band(self):
        cursor = connection.cursor()            
        cursor.execute(self.get_sql_text())             
        master = MasterBand()
        master.query = self.dictfetchall(cursor)
        cursor.close()
        master.add_component(type = "dataP", name='nmproduto', db_link='nmproduto', 
            style="margin:3px 5px 3px 43px;float:left;width:50%")
        return master

    def get_sql_text(self):
        sql_text = '''
            SELECT itc.dsproduto AS cardapio__dsproduto, agra.nmagrupadic AS agrupadicional__nmagrupadic, prod.nmproduto,
                   itc.id AS id_adic, agra.id AS id_agra
              FROM public."Adicionais" AS adic
             INNER JOIN  public."AgrupAdicional" AS agra
                 ON adic.agrupadicional_id = agra.id
             INNER JOIN public.itagrupadicional AS itag
                 ON agra.id = itag.agrupadicional_id
             INNER JOIN public."ItemCategoria" itc
                 ON itag.cardapio_id = itc.id
             INNER JOIN public.Produto AS prod
                ON adic.item_id = prod.id
             ORDER BY itc.id, agra.id, itc.dsproduto, agra.nmagrupadic, prod.nmproduto '''
        return sql_text
  

    def Print(self):
        try:
            report = Report(page_header = self.get_header(), master_band = self.get_master_band(), template="", page_title = "Cardápio / Agrupamentos",
                            group_headers=[self.get_group_header_cardapio(), self.get_group_header_agrupadicional()])
            return HttpResponse(report.as_html() )
        except Exception as e:
            return HttpResponse(e)

@login_required
def RelCardapio(request):
    rel = CardapioRel()
    return rel.Print()
