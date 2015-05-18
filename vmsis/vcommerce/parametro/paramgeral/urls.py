# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView, ViewUpdate, ConvertView, urlsCrud
from parametro.paramgeral.models import Paramgeral
from parametro.paramgeral.views import ParamGeralView

class CrudUpd(CrudView):
    def __init__(self, model):
        self.model = model
        self.view = ConvertView(model)
        self.UrlCrud = urlsCrud(model);

    def AsUrl(self, MediaFilesUpdate = ['paramgeral.js'],  ClassUpdate = ViewUpdate):
        urls = patterns('', 
            url(self.UrlCrud.UrlUpdate(), self.view.Update(MediaFiles = MediaFilesUpdate, ClassView = ClassUpdate)))
        return urls

Crud = CrudUpd(Paramgeral)

urlpatterns = Crud.AsUrl(ClassUpdate = ParamGeralView)



