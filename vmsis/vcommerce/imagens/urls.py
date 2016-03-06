from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'^imagens/Lista', 'imagens.views.ObterImagens'), )