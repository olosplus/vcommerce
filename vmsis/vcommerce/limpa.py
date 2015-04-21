#!/opt/workspace/vtestes/vmsis/bin/python3.3
# -*- coding: utf8 -*- 

import subprocess, os

try:
    print("\nIniciando limpeza...")
    return_code = subprocess.call('find -iname "__pycache__" -exec rm -rfv {} \\;', shell=True)
    print("\nApagando banco de dados...")
    if (os.path.exists('db.sqlite3')):
        return_code = subprocess.call('rm db.sqlite3', shell=True)    
    print("\nPronto!")

except KeyboardInterrupt:
	print("\nOperação cancelada!\n\n")