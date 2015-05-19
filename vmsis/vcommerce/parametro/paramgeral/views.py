# -*- coding: utf-8 -*- 
from vlib.view_lib import TEMPLATE_UPDATE, CrudView, ViewUpdate, ConvertView, urlsCrud
from django.conf.urls import patterns, include, url


class ConvertViewParam(ConvertView):
    def Update(self, MediaFiles = [],  ClassView = ViewUpdate):

        return ClassView.as_view(model = self.model, success_url = '', 
            template_name = TEMPLATE_UPDATE, MediaFiles = MediaFiles)
    
class CrudUpd(CrudView):
    def __init__(self, model):
        self.model = model
        self.view = ConvertViewParam(model)
        self.UrlCrud = urlsCrud(model);

    def AsUrl(self, MediaFilesUpdate = ['js/paramgeral.js'],  ClassUpdate = ViewUpdate):
        urls = patterns('', 
            url(self.UrlCrud.UrlUpdate(), self.view.Update(MediaFiles = MediaFilesUpdate, ClassView = ClassUpdate)))
        return urls
