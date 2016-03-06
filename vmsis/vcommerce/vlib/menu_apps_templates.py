from django.conf import settings
from django.apps import apps as apps_on_project
from vlib import menu_apps
import os

    
DIR = settings.BASE_DIR
TAG_DROP = "<span class='fa arrow'></span>"
TAG_UL_SEC = "<ul class='nav nav-second-level'>"
TAG_UL_THI = "<ul class='nav nav-third-level'>"
TAG_UL = "<ul>"
TAG_LI = "<li>"
CLOSE_TAG_LI = "</li>"
TAG_I = "<i "
CLOSE_TAG_I = "</i>"
CLOSE_TAG_UL = "</ul>"
TAG_A_PARTIAL = "<a"
TAG_A = "<a>"
CLOSE_TAG_A = "</a>"
ATTR_HREF = "href="
CLOSE_TAG = ">"
OPEN_TAG = "<"

class MenuAppsTemplate(object):   

    def __init__(self, permissoes = None):
        self.permissoes = permissoes
    
    
    def has_model(self, directory):
        """Verifica se há o arquivo models.py no diretório informado"""
        return os.path.isfile(directory + '/models.py')
    
    def has_url(self, directory):
        """Verifica se há o arquivo urls.py no diretório informado"""
        return os.path.isfile(directory + '/urls.py')
    
    def load_urls_patterns(self, patterns):
        """Retorna a lista de configurações das urls do patterns passado no parâmetro"""
        URL_NAMES = []
        for pat in patterns:
            if pat.__class__.__name__ == 'RegexURLPattern':
                URL_NAMES.append(pat.regex.pattern)
        return URL_NAMES
    
    def get_app_name_on_path(self, path):
        position_path_app = len(DIR) + 1
        tree_app = ''.join(path[position_path_app:])
        tree_app = tree_app.replace("/", ".")
        return tree_app
    
    def module_exists(self, module_name):
        try:
            __import__(module_name, fromlist = ['no_module_list'])
        except ImportError:
            return False
        else:
            return True        
    
    def load_url_app(self, path_app):
        """Retorna a primeira url da lista de urls configuradas para o app situado no diretório 
           completo informado no parâmetro
        """
        if not self.has_url(path_app):
            return "javascript:void(0)"
        tree_app = self.get_app_name_on_path(path_app) #tree_app.replace("/", ".")
        urls = []
        app = __import__(tree_app, fromlist=['no_module_list'])    
        if app:
            if hasattr(app, 'urls'):
                if app.urls.urlpatterns:        
                    urls = self.load_urls_patterns(app.urls.urlpatterns)                
        if urls:
            return  "/" + urls[0].split('.')[0].replace("^", "")
        else:  
            return "javascript:void(0)"
    
    def installed_apps(self):
        """ Retorna a lista com o nome do app. Apenas o nome, não retorna a árvore de módulos completa"""
        lapps = []
        for app in settings.INSTALLED_APPS  :
            for nome_app in app.split("."):
                lapps.append(nome_app)
            else:
                lapps.append(app)
        return lapps
    
       
    def get_apps_html(self, path, hab_UL=False, nivel=1, empresa=None, menu=True):
                        
        NAME_APPS_INSTALLED = self.installed_apps() 
        """ monta o html do menu"""
        html = ""
        abrir_ul = False
        url_app = ""
        if os.path.isdir(path):
            try:
                dirs = next(os.walk(path))[1]
                dirs.sort()
            except PermissionError:
                dirs = []
            for directory in dirs:
                #return bool_apps_filho(directory)
                app_name = self.get_app_name_on_path(path + "/" + directory)
                if directory in NAME_APPS_INSTALLED:                    
                    if not menu_apps.MenuApps.AppIsVisible(app_name) or not self.permissoes.get_permissao(app_label=directory, permission_type='show'):
                        continue
                    
                    if hab_UL:
                        if not abrir_ul:
                            nivel+=1
                            if menu:
                                if nivel == 2:
                                   html += TAG_UL_SEC
                                else:
                                   html += TAG_UL_THI
                            else:
                                html += TAG_UL
                            abrir_ul = True
                    
                    if html:
                        html += "<li data-module='%s'>" % app_name
    
                    url_app = self.load_url_app(path + "/" + directory)
                    
                    if app_name == 'parametro.paramgeral':
                        url_app = url_app.replace('(?P<pk>\d+)/$',str(empresa))
                    
                    if menu:
                        html += "%s href='javascript:void(0)' onclick='openPage(\"%s\", \"%s\", \"%s\")' %s" % \
                            (TAG_A_PARTIAL, app_name, url_app, menu_apps.MenuApps.GetAppVerboseName(app_name), 
                                CLOSE_TAG_A)
                    
                    
                    
                    if menu_apps.MenuApps.ImgMenuApp(app_name):
                        html += "%s class='%s'> %s" % (TAG_I, menu_apps.MenuApps.ImgMenuApp(app_name),CLOSE_TAG_I)
                    if menu:
                        html += ' '+menu_apps.MenuApps.GetAppVerboseName(app_name)
                    else:
                        html += '<a href="javascript:void(0)" class="black">'+menu_apps.MenuApps.GetAppVerboseName(app_name)+ '</a>'
                    
                    if self.bool_apps_filho(path + "/" + directory):
                        html += TAG_DROP
                    
                    if menu:
                        html += CLOSE_TAG_A
                        
                    html += self.get_apps_html(path=path + "/" + directory, hab_UL=True, nivel=nivel, empresa=empresa, menu=menu )
                    
                    if html:
                        html += CLOSE_TAG_LI
            if abrir_ul:
                html += CLOSE_TAG_UL
                nivel-=1
        return html  
    
    
    
    def bool_apps_filho(self, path_app):
        """ verifica se aplicacao tem filho"""
        LIST_APPS_MENUS = menu_apps.MenuApps.GetAppsOnMenu(only_visible=True)    
        dirs = next(os.walk(path_app))[1]
        for directory in dirs:
            tree_app = self.get_app_name_on_path(path_app + "/"+ directory)
    
            if tree_app in LIST_APPS_MENUS:
                return True
    
        return False
    
    