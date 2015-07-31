# coding: utf-8
from django.conf.urls import patterns, include, url
import os 
from django.db import models
from vcommerce import apps
from vlib import urls as vlib_urls
import json

models.options.DEFAULT_NAMES += ('child_models', 'exclude_fk_plus')

DIR = os.path.dirname(os.path.dirname(__file__))

MAIN_APP = {'app': 'vlib', 'verbose_name': 'Home', 'view_name': 'vlib.views.index' }

apps_on_menu = apps.apps_on_menu

class MenuApps:       
    @staticmethod
    def GetAppsOnMenu(only_visible = False):
        apps = ()
        
        for app in apps_on_menu:
            if only_visible and 'visible' in app:
                if not app['visible']:
                    continue                

            apps += (app['app'], )
        return apps

    @staticmethod
    def GetAppsVerboseName(only_visible = False):

        apps_str = '{'

        for app in apps_on_menu:
            if(only_visible):
                if(MenuApps.AppIsVisible(app['app'])):
                    apps_str +=  '"%s":"%s",' % (app['app'], app['verbose_name'] )
            else:
                apps_str +=  '"%s":"%s",' % (app['app'], app['verbose_name'] )

        apps_str += ' "end-of-dict":""}'

        return json.loads(apps_str)


    @staticmethod
    def IncludeUrls():
        patt = patterns('', url(r'^$', MAIN_APP['view_name']),)
        patt += patterns('', url(r'', include(vlib_urls)  ),)        
        for app in apps_on_menu:
            if os.path.isfile(DIR + "/" + app['app'].replace(".", "/") + "/urls.py"):
                patt += patterns('', url(r'', include(app['app'] + '.urls', 'teste')),)
        return patt
   
    @staticmethod
    def GetAppVerboseName(app_name):
        for app in apps_on_menu:
            if app['app'].upper() == app_name.upper():
           	    return app['verbose_name']

    @staticmethod
    def AppIsVisible(app_name):
        for app in apps_on_menu:            
            if app['app'].upper() == app_name.upper():                
                if 'visible' in app:
                    return app['visible']
                else:
                    return True
        return False

    @staticmethod
    def AppIsVisibleByAppLabel(app_label):        
        for app in apps_on_menu:
            list_module = app['app'].split(".")           
            if list_module[len(list_module)-1].upper() == app_label.upper():                
                if 'visible' in app:
                    return app['visible']
                else:
                    return True
        return False
    
    
    @staticmethod
    def ImgMenuApp(app_name):
        for app in apps_on_menu:
            if app['app'].upper() == app_name.upper():
                if 'imgmenu' in app:
                    return app['imgmenu']
                else:
                    return ''
