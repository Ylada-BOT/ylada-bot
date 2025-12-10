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

# Trata erros de importação de forma mais robusta
try:
    # Importa o app Flask (com suporte a /qr e Render)
    # Para usar versão multi-instance, mude para: from web.app_multi import app
    from web.app import app
except Exception as e:
    # Se falhar, tenta criar um app mínimo
    print(f"[!] Erro ao importar app: {e}")
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/', methods=['GET'])
    def error_handler():
        return {
            "error": "Erro ao inicializar aplicação",
            "message": str(e),
            "status": "error"
        }, 500

# Para Vercel, exportamos o app diretamente
# O @vercel/python detecta automaticamente

