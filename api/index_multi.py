"""
Vercel Serverless Function Entry Point - Multi-Instance
Suporta múltiplas instâncias WhatsApp (4+ telefones)
"""
import sys
import os

# Adiciona o diretório raiz ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, 'src'))

# Importa o app Flask multi-instance
from web.app_multi import app

# Para Vercel, exportamos o app diretamente
# O @vercel/python detecta automaticamente

