from django.conf.urls import patterns, url

urlpatterns = patterns('', url('getmodelasxml/', 'sincronizacao.views.GetModelAsXML' ),)
urlpatterns += patterns('', url('savejsonasmodel/', 'sincronizacao.views.SaveJsonAsModel' ),)
