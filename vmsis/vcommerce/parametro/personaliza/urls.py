# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from parametro.personaliza.views import ParamUpdate

urlpatterns = patterns('',
    url(r'parametro/personaliza/1', ParamUpdate.as_view(), name='ParamUpdate'),
    #url(r'insert/', cadastro.views.PadInsert.as_view(), name='PadInsert'),
    #url(r'delete/(?P<pk>\d+)/$', cadastro.views.PadDelete.as_view(), name='PadDelete'),
    #url(r'update/(?P<pk>\d+)/$', cadastro.views.PadUpdate.as_view(), name='PadUpdate'),
)