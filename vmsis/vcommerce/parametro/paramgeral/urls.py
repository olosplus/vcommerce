# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from vlib.view_lib import CrudView, ViewUpdate
from parametro.paramgeral.models import Paramgeral

class CrudUpd(CrudView):
	def AsUrl(self, MediaFilesUpdate = [], ClassUpdate = ViewUpdate):

		urls = patterns('', 
			url(self.UrlCrud.UrlUpdate(), self.view.Update(MediaFiles = MediaFilesUpdate, ClassView = ClassUpdate)))
		return urls

Crud = CrudUpd(Paramgeral)

urlpatterns = Crud.AsUrl()