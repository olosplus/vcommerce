# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from vlib import menu_apps, urls

urlpatterns = patterns('',
    url(r'^login/', 'django.contrib.auth.views.login', {"template_name": "login.html"}),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/login/'}),
)

urlpatterns += menu_apps.MenuApps.IncludeUrls();