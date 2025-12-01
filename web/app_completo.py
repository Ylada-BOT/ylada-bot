"""
API Flask Completa - Bot Ylada
VERSÃO COMPLETA - Mantida como referência

Esta versão tem todas as funcionalidades:
- Múltiplos modos (simple, web, webjs, zapi)
- Integração WhatsApp Web.js
- Integração Z-API
- Múltiplas instâncias
- Todas as features avançadas

Use app.py para a versão simplificada (atual).
Use este arquivo como referência quando precisar de funcionalidades avançadas.
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bot import LadaBot

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
CORS(app)

# Inicializa o bot
# Modos disponíveis: "simple" (gratuito), "web" (WhatsApp Web gratuito), "webjs" (WhatsApp Web.js gratuito), "zapi" (pago)
BOT_MODE = os.getenv("BOT_MODE", "simple")  # Padrão: modo simples (gratuito)
bot = LadaBot(
    config_path=os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml'),
    mode=BOT_MODE
)


@app.route('/', methods=['GET'])
def index():
    """Página inicial do dashboard"""
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({"status": "ok", "bot": "Ylada"})


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """
    Webhook do Z-API
    
    GET: Verificação do webhook
    POST: Recebe mensagens
    """
    if request.method == 'GET':
        # Verificação do webhook (Z-API pode enviar token)
        verify_token = request.args.get('token')
        # Aqui você pode validar o token se necessário
        return jsonify({"status": "ok"}), 200
    
    # POST: Processa mensagem
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data"}), 400
        
        response = bot.handle_webhook(data)
        return jsonify({"status": "processed", "response": response}), 200
    
    except Exception as e:
        print(f"[!] Erro no webhook: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/send', methods=['POST'])
def send_message():
    """
    Endpoint para enviar mensagem manualmente (para testes)
    
    Body:
        {
            "phone": "5511999999999",
            "message": "Olá!"
        }
    """
    try:
        data = request.get_json()
        phone = data.get("phone")
        message = data.get("message")
        
        if not phone or not message:
            return jsonify({"error": "phone and message are required"}), 400
        
        success = bot.send_message(phone, message)
        return jsonify({"success": success}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/contacts', methods=['GET'])
def contacts_page():
    """Página de gerenciamento de contatos"""
    return render_template('contacts.html')


@app.route('/conversations', methods=['GET'])
def get_conversations():
    """Lista conversas ativas"""
    # Se for requisição HTML, retorna página formatada
    if 'text/html' in request.headers.get('Accept', ''):
        return render_template('conversations.html')
    
    # Se for JSON (API)
    conversations = bot.conversation.conversations
    
    # Se for modo simples, adiciona log de mensagens
    if bot.mode == "simple" and hasattr(bot.whatsapp, 'get_messages_log'):
        messages_log = bot.whatsapp.get_messages_log()
    else:
        messages_log = []
    
    return jsonify({
        "conversations": conversations,
        "mode": bot.mode,
        "messages_log": messages_log
    }), 200


@app.route('/contacts', methods=['GET'])
def get_contacts():
    """Lista contatos com filtros"""
    category = request.args.get('category')
    tag = request.args.get('tag')
    search = request.args.get('search')
    
    contacts = bot.contacts.list_contacts(category=category, tag=tag, search=search)
    stats = bot.contacts.get_stats()
    
    return jsonify({
        "contacts": contacts,
        "stats": stats,
        "total": len(contacts)
    }), 200


@app.route('/contacts/<phone>', methods=['GET'])
def get_contact(phone):
    """Obtém informações de um contato específico"""
    contact = bot.contacts.get_contact(phone)
    if not contact:
        return jsonify({"error": "Contato não encontrado"}), 404
    return jsonify(contact), 200


@app.route('/contacts/<phone>', methods=['PUT'])
def update_contact(phone):
    """Atualiza informações de um contato"""
    data = request.get_json()
    
    if 'name' in data:
        contact = bot.contacts.get_or_create_contact(phone, data['name'])
    
    if 'tags' in data:
        # Remove tags antigas e adiciona novas
        contact = bot.contacts.get_contact(phone)
        if contact:
            for tag in contact.get('tags', []):
                bot.contacts.remove_tag(phone, tag)
            for tag in data['tags']:
                bot.contacts.add_tag(phone, tag)
    
    if 'category' in data:
        bot.contacts.set_category(phone, data['category'])
    
    if 'notes' in data:
        bot.contacts.set_notes(phone, data['notes'])
    
    return jsonify({"success": True}), 200


@app.route('/contacts/<phone>/tags', methods=['POST'])
def add_tag_to_contact(phone):
    """Adiciona tag a um contato"""
    data = request.get_json()
    tag = data.get('tag')
    if not tag:
        return jsonify({"error": "Tag é obrigatória"}), 400
    
    bot.contacts.add_tag(phone, tag)
    return jsonify({"success": True}), 200


@app.route('/contacts/<phone>/tags/<tag>', methods=['DELETE'])
def remove_tag_from_contact(phone, tag):
    """Remove tag de um contato"""
    bot.contacts.remove_tag(phone, tag)
    return jsonify({"success": True}), 200


@app.route('/contacts/export', methods=['GET'])
def export_contacts():
    """Exporta contatos para CSV"""
    filepath = os.path.join('data', 'contacts_export.csv')
    success = bot.contacts.export_contacts_csv(filepath)
    
    if success:
        from flask import send_file
        return send_file(filepath, as_attachment=True, download_name='contatos_ylada.csv')
    else:
        return jsonify({"error": "Erro ao exportar"}), 500


@app.route('/contacts/stats', methods=['GET'])
def get_contacts_stats():
    """Retorna estatísticas dos contatos"""
    stats = bot.contacts.get_stats()
    return jsonify(stats), 200


@app.route('/connect', methods=['POST'])
def connect_whatsapp():
    """Conecta ao WhatsApp Web (apenas modo web)"""
    if bot.mode != "web":
        return jsonify({"error": "Modo web não ativado"}), 400
    
    success = bot.connect_whatsapp()
    return jsonify({"success": success}), 200


@app.route('/qr', methods=['GET'])
def qr_code_page():
    """Página para escanear QR Code do WhatsApp Web.js"""
    if bot.mode != "webjs":
        return jsonify({"error": "Modo webjs não ativado"}), 400
    return render_template('qr_code.html')


@app.route('/api/qr', methods=['GET'])
def get_qr_code():
    """API para obter QR Code (proxy para servidor Node.js)"""
    try:
        import requests
        response = requests.get('http://localhost:3000/qr', timeout=5)
        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({"error": str(e), "qr": None, "ready": False}), 500


@app.route('/api/whatsapp-status', methods=['GET'])
def get_whatsapp_status():
    """API para obter status do WhatsApp (proxy para servidor Node.js)"""
    try:
        import requests
        response = requests.get('http://localhost:3000/status', timeout=5)
        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({"error": str(e), "ready": False, "hasQr": False}), 500


@app.route('/test', methods=['GET'])
def test_page():
    """Página de testes dos endpoints"""
    return render_template('test.html')


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    print(f"\n🚀 Bot Ylada (COMPLETO) rodando em http://localhost:{port}")
    print(f"📡 Health check: http://localhost:{port}/health")
    print(f"🔗 Webhook: http://localhost:{port}/webhook")
    print(f"📖 Dashboard: http://localhost:{port}\n")
    app.run(host='0.0.0.0', port=port, debug=True)
