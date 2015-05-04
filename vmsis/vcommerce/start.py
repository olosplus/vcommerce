#!/opt/workspace/vtestes/vmsis/bin/python3.3
# -*- coding: utf8 -*- 

import subprocess, os

try:
    print(input("\nAtenção, não use o start em produção! (Ctrl+C para sair)\n"))
    if (os.path.exists('db.sqlite3')):
    	if input("Deseja excluir o banco de dados existente? (Default=N)").capitalize()=="S":
    		print("\nRemovendo banco de dados...")
    		return_code = subprocess.call('rm db.sqlite3', shell=True)
    
    print("\nIdentificando e criando os arquivos de migração")
    return_code = subprocess.call('python manage.py makemigrations', shell=True)
    print("\nGerenciando a evolução dos models e schemas...")
    return_code = subprocess.call('python manage.py migrate', shell=True)
    
    if input("Deseja criar um super usuário? (Default=N)").capitalize()=="S":
        print("\nCriando usuário principal...")
        return_code = subprocess.call('python manage.py createsuperuser', shell=True)

    print("\nAlimentando tabelas:")
    print("\nPaís...")
    return_code = subprocess.call('python manage.py loaddata cadastro/fix/pais.json', shell=True)
    print("\nEstado...")
    return_code = subprocess.call('python manage.py loaddata cadastro/fix/estado.json', shell=True)
    print("\nCidade...")
    return_code = subprocess.call('python manage.py loaddata cadastro/fix/cidade.json', shell=True)
    #print("\nBairro...")
    #return_code = subprocess.call('python manage.py loaddata cadastro/fix/bairro.json', shell=True)
    print("\nBanco...")
    return_code = subprocess.call('python manage.py loaddata cadastro/fix/banco.json', shell=True)
    print("\nCentro de Custo...")
    return_code = subprocess.call('python manage.py loaddata cadastro/fix/centrodecusto.json', shell=True)
    print("\nUnidade de Medida...")
    return_code = subprocess.call('python manage.py loaddata cadastro/fix/unimedida.json', shell=True)

    #print("\nCadastros Samanta...")
    #return_code = subprocess.call('python manage.py loaddata cadastro/fix/samanta.json', shell=True)

    print("\nIniciando serviço...")
    return_code = subprocess.call('python manage.py runserver', shell=True)

except KeyboardInterrupt:
	print("\nOperação cancelada!\n\n")