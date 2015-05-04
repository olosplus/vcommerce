# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('', url('savegrid/', 'vlib.views.save_grid'),)
urlpatterns += patterns('', url('deletegrid/', 'vlib.views.delete_grid'),)
urlpatterns += patterns('', url('filtro/', 'vlib.views.Filtro'),)
urlpatterns += patterns('', url('getgrid/', 'vlib.views.GetGridCrud'),)
urlpatterns += patterns('', url('mudarunidade/', 'vlib.views.SetUnidade'),)


