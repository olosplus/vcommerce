# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from parametro.paramgeral.models import Paramgeral
from parametro.paramgeral.views import CrudUpd

Crud = CrudUpd(Paramgeral)

urlpatterns = Crud.AsUrl()



