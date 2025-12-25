"""
Entrypoint para Vercel
Importa o app Flask de web/app.py
"""
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa o app Flask
from web.app import app

# Exporta para Vercel
application = app

# Handler para Vercel
def handler(request):
    return application


