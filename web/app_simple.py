"""
BOT by YLADA
Integração WhatsApp + Inteligência Artificial

Simples: Conecte WhatsApp, configure IA, receba respostas automáticas.
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from whatsapp_webjs_handler import WhatsAppWebJSHandler
from ai_handler import AIHandler

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'),
            static_url_path='/static')
CORS(app)

# ============================================
# INICIALIZAÇÃO
# ============================================

# WhatsApp Handler
whatsapp = None
try:
    whatsapp = WhatsAppWebJSHandler(instance_name="ylada_bot", port=5001)
    print("[✓] WhatsApp Handler inicializado")
except Exception as e:
    print(f"[!] Erro ao inicializar WhatsApp: {e}")

# IA Handler
ai = AIHandler()
print("[✓] IA Handler inicializado")

# Configuração (salva em arquivo simples)
CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'ai_config.json')

def load_config():
    """Carrega configuração da IA"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                ai.set_config(
                    provider=config.get('provider', 'openai'),
                    api_key=config.get('api_key', ''),
                    model=config.get('model', 'gpt-4o-mini'),
                    system_prompt=config.get('system_prompt', 'Você é um assistente útil e amigável.')
                )
                return config
        except:
            pass
    return {
        'provider': 'openai',
        'api_key': '',
        'model': 'gpt-4o-mini',
        'system_prompt': 'Você é um assistente útil e amigável.'
    }

def save_config(config):
    """Salva configuração da IA"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

# Carrega configuração ao iniciar
load_config()

# ============================================
# ROTAS - DASHBOARD
# ============================================

@app.route('/')
def index():
    """Dashboard principal - SIMPLES"""
    config = load_config()
    
    # Verifica status do WhatsApp - SEMPRE começa como desconectado
    # O status será verificado via JavaScript em tempo real
    # Isso evita mostrar "Conectado" quando não está
    return render_template('dashboard_simple.html')

# ============================================
# ROTAS - WHATSAPP
# ============================================

@app.route('/qr')
def qr_code():
    """Página para escanear QR Code"""
    return render_template('qr_simple.html')

@app.route('/api/qr')
def get_qr():
    """Obtém QR Code do WhatsApp"""
    if not whatsapp:
        return jsonify({"error": "WhatsApp não inicializado"}), 500
    
    try:
        qr_data = whatsapp.get_qr_code()
        if qr_data:
            return jsonify({"qr": qr_data, "status": "waiting"})
        else:
            # Verifica se já está conectado
            if whatsapp.is_ready():
                return jsonify({"status": "connected"})
            return jsonify({"status": "generating"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/whatsapp-status')
def whatsapp_status():
    """Status da conexão WhatsApp"""
    if not whatsapp:
        return jsonify({"connected": False, "error": "WhatsApp não inicializado"})
    
    try:
        connected = whatsapp.is_ready()
        return jsonify({"connected": connected})
    except Exception as e:
        return jsonify({"connected": False, "error": str(e)})

# ============================================
# ROTAS - IA
# ============================================

@app.route('/api/ai/config', methods=['GET'])
def get_ai_config():
    """Obtém configuração da IA"""
    config = load_config()
    # Não retorna API key por segurança
    return jsonify({
        'provider': config.get('provider'),
        'model': config.get('model'),
        'system_prompt': config.get('system_prompt'),
        'configured': bool(config.get('api_key'))
    })

@app.route('/api/ai/config', methods=['POST'])
def set_ai_config():
    """Configura a IA"""
    data = request.get_json()
    
    config = {
        'provider': data.get('provider', 'openai'),
        'api_key': data.get('api_key', ''),
        'model': data.get('model', 'gpt-4o-mini'),
        'system_prompt': data.get('system_prompt', 'Você é um assistente útil e amigável.')
    }
    
    # Atualiza handler
    ai.set_config(
        provider=config['provider'],
        api_key=config['api_key'],
        model=config['model'],
        system_prompt=config['system_prompt']
    )
    
    # Salva configuração
    save_config(config)
    
    return jsonify({"success": True, "message": "Configuração salva!"})

# ============================================
# ROTAS - WEBHOOK (MENSAGENS)
# ============================================

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook que recebe mensagens do WhatsApp
    Processa com IA e envia resposta automática
    """
    try:
        data = request.get_json()
        
        # Extrai dados da mensagem
        phone = data.get('from') or data.get('phone')
        message = data.get('body') or data.get('message')
        
        if not phone or not message:
            return jsonify({"error": "Dados inválidos"}), 400
        
        # Remove formatação do número
        phone = phone.replace('@s.whatsapp.net', '').replace('@c.us', '').replace('+', '').replace(' ', '')
        
        print(f"[📨] Mensagem recebida de {phone}: {message}")
        
        # Verifica se IA está configurada
        config = load_config()
        if not config.get('api_key'):
            print("[!] IA não configurada. Configure no dashboard primeiro.")
            return jsonify({
                "success": False,
                "error": "IA não configurada"
            }), 400
        
        # Obtém resposta da IA
        try:
            response = ai.get_response(phone, message)
            print(f"[🤖] Resposta da IA: {response}")
            
            # Envia resposta via WhatsApp
            if whatsapp and response:
                success = whatsapp.send_message(phone, response)
                if success:
                    print(f"[✓] Resposta enviada para {phone}")
                else:
                    print(f"[!] Erro ao enviar resposta para {phone}")
        except Exception as e:
            print(f"[!] Erro ao processar com IA: {e}")
            return jsonify({"error": str(e)}), 500
        
        return jsonify({
            "success": True,
            "response": response
        })
        
    except Exception as e:
        print(f"[!] Erro no webhook: {e}")
        return jsonify({"error": str(e)}), 500

# ============================================
# ROTAS - UTILITÁRIOS
# ============================================

@app.route('/health')
def health():
    """Health check"""
    return jsonify({"status": "ok"})

# ============================================
# INICIALIZAÇÃO DO SERVIDOR WHATSAPP
# ============================================

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🔗 BOT by YLADA")
    print("="*50)
    print("\n📱 Automação com WhatsApp")
    print("\n✨ Funcionalidades:")
    print("  1. Conecte WhatsApp (QR Code)")
    print("  2. Configure IA (API Key)")
    print("  3. IA responde automaticamente")
    print("\n" + "="*50 + "\n")
    
    # Tenta iniciar servidor WhatsApp automaticamente
    if whatsapp:
        try:
            print("[*] Iniciando servidor WhatsApp...")
            if whatsapp.start_server():
                print("[✓] Servidor WhatsApp iniciado com sucesso!")
            else:
                print("[!] Servidor WhatsApp pode não ter iniciado. Verifique os logs.")
        except Exception as e:
            print(f"[!] Erro ao iniciar servidor WhatsApp: {e}")
            print("[!] Você pode iniciar manualmente com: node whatsapp_server.js")
    
    # Inicia Flask
    port = int(os.getenv('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=True)

