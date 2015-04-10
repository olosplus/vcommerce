#!/usr/bin/python
# -*- coding: utf8 -*- 

import subprocess

print("\nGerenciando a evolução dos models e schemas...")
return_code = subprocess.call('python manage.py migrate', shell=True)
print("\nConferindo sincronização e criando usuário principal caso não exista...")
return_code = subprocess.call('python manage.py syncdb', shell=True)
print("\nIdentificando e criando os arquivos de migração")
return_code = subprocess.call('python manage.py makemigrations', shell=True)

print("\n\nAlimentando tabelas:")
print("\nPaís...")
return_code = subprocess.call('python manage.py loaddata cadastro/fix/pais.json', shell=True)

print("\nIniciando serviço...")
return_code = subprocess.call('python manage.py runserver', shell=True)