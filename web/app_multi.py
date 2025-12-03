"""
API Flask - Ylada BOT Multi-Instance
Suporta múltiplas instâncias WhatsApp (4+ telefones)
Arquitetura SaaS-ready
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os
import time
import json
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database import Database
from instance_manager import InstanceManager
from account_manager import AccountManager
from bot_simple import LadaBotSimple

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
CORS(app)

# Inicializa componentes
db = Database(use_sqlite=True)  # Mude para False para usar PostgreSQL
account_manager = AccountManager(db)
instance_manager = InstanceManager(db)

# Inicia monitoramento automático
instance_manager.start_monitoring(interval=30)

# Bot simplificado (para compatibilidade)
bot = LadaBotSimple(config_path=os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml'))


# ========== ROTAS PRINCIPAIS ==========

@app.route('/', methods=['GET'])
def index():
    """Dashboard principal - Multi-instância"""
    return render_template('index_multi.html')


@app.route('/health', methods=['GET'])
def health():
    """Status do servidor"""
    return jsonify({
        "status": "ok",
        "bot": "Ylada BOT Multi-Instance",
        "instances_count": len(instance_manager.instances)
    })


# ========== API DE INSTÂNCIAS ==========

@app.route('/api/instances', methods=['GET'])
def list_instances():
    """Lista todas as instâncias (seus 4 telefones)"""
    try:
        instances = instance_manager.get_all_instances_status()
        return jsonify({
            'success': True,
            'instances': instances,
            'total': len(instances)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/instances/<account_id>/start', methods=['POST'])
def start_instance(account_id: str):
    """Inicia instância de uma conta"""
    try:
        success = instance_manager.start_instance(account_id)
        return jsonify({'success': success}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/instances/<account_id>/stop', methods=['POST'])
def stop_instance(account_id: str):
    """Para instância de uma conta"""
    try:
        success = instance_manager.stop_instance(account_id)
        return jsonify({'success': success}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/instances/<account_id>/status', methods=['GET'])
def get_instance_status(account_id: str):
    """Retorna status da instância"""
    try:
        status = instance_manager.get_instance_status(account_id)
        if status:
            return jsonify({'success': True, 'status': status}), 200
        else:
            return jsonify({'success': False, 'error': 'Instância não encontrada'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/instances/<account_id>/qr', methods=['GET'])
def get_instance_qr(account_id: str):
    """Retorna QR Code da instância"""
    try:
        handler = instance_manager.get_instance(account_id)
        if not handler:
            return jsonify({'success': False, 'error': 'Instância não encontrada'}), 404
        
        # Inicia servidor se não estiver rodando
        if not handler.is_ready():
            handler.start_server()
            time.sleep(3)  # Aguarda gerar QR
        
        qr = handler.get_qr_code()
        is_ready = handler.is_ready()
        
        return jsonify({
            'success': True,
            'qr': qr,
            'ready': is_ready,
            'message': 'WhatsApp conectado!' if is_ready else 'Escaneie o QR Code'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== API DE CONTAS ==========

@app.route('/api/accounts', methods=['GET'])
def list_accounts():
    """Lista todas as contas"""
    try:
        accounts = account_manager.get_all_accounts()
        return jsonify({
            'success': True,
            'accounts': accounts,
            'total': len(accounts)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<account_id>', methods=['GET'])
def get_account(account_id: str):
    """Retorna dados da conta"""
    try:
        account = account_manager.get_account(account_id)
        if account:
            return jsonify({'success': True, 'account': account}), 200
        else:
            return jsonify({'success': False, 'error': 'Conta não encontrada'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== API DE CONTATOS (Isolado por conta) ==========

@app.route('/api/accounts/<account_id>/contacts', methods=['GET'])
def get_account_contacts(account_id: str):
    """Retorna contatos da conta (isolado)"""
    try:
        contacts = account_manager.get_account_contacts(account_id)
        return jsonify({
            'success': True,
            'contacts': contacts,
            'total': len(contacts)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<account_id>/contacts', methods=['POST'])
def create_contact(account_id: str):
    """Cria contato na conta"""
    try:
        data = request.get_json()
        contact = account_manager.create_contact(
            account_id=account_id,
            phone=data.get('phone'),
            name=data.get('name'),
            tags=data.get('tags', [])
        )
        return jsonify({'success': True, 'contact': contact}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== API DE CAMPANHAS (Isolado por conta) ==========

@app.route('/api/accounts/<account_id>/campaigns', methods=['GET'])
def get_account_campaigns(account_id: str):
    """Retorna campanhas da conta (isolado)"""
    try:
        campaigns = account_manager.get_account_campaigns(account_id)
        return jsonify({
            'success': True,
            'campaigns': campaigns,
            'total': len(campaigns)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<account_id>/campaigns', methods=['POST'])
def create_campaign(account_id: str):
    """Cria campanha na conta"""
    try:
        data = request.get_json()
        campaign = account_manager.create_campaign(
            account_id=account_id,
            name=data.get('name'),
            message=data.get('message'),
            qr_code_url=data.get('qr_code_url'),
            link=data.get('link')
        )
        return jsonify({'success': True, 'campaign': campaign}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== API DE CONVERSAS (Isolado por conta) ==========

@app.route('/api/accounts/<account_id>/conversations', methods=['GET'])
def get_account_conversations(account_id: str):
    """Retorna conversas da conta (isolado)"""
    try:
        limit = request.args.get('limit', 100, type=int)
        conversations = account_manager.get_account_conversations(account_id, limit)
        return jsonify({
            'success': True,
            'conversations': conversations,
            'total': len(conversations)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== API DE MENSAGENS ==========

@app.route('/api/accounts/<account_id>/send', methods=['POST'])
def send_message(account_id: str):
    """Envia mensagem via instância da conta"""
    try:
        data = request.get_json()
        phone = data.get('phone')
        message = data.get('message')
        
        if not phone or not message:
            return jsonify({'success': False, 'error': 'phone and message are required'}), 400
        
        success = instance_manager.send_message(account_id, phone, message)
        
        if success:
            # Registra conversa
            account_manager.create_conversation(
                account_id=account_id,
                contact_id=None,  # Pode buscar depois
                message=message,
                from_me=True
            )
        
        return jsonify({'success': success}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<account_id>/chats', methods=['GET'])
def get_chats(account_id: str):
    """Retorna chats da instância"""
    try:
        chats = instance_manager.get_chats(account_id)
        return jsonify({
            'success': True,
            'chats': chats,
            'total': len(chats)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/accounts/<account_id>/chats/<chat_id>/messages', methods=['GET'])
def get_chat_messages(account_id: str, chat_id: str):
    """Retorna mensagens de um chat"""
    try:
        limit = request.args.get('limit', 50, type=int)
        messages = instance_manager.get_chat_messages(account_id, chat_id, limit)
        return jsonify({
            'success': True,
            'messages': messages,
            'total': len(messages)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== COMPATIBILIDADE (Rotas antigas) ==========

@app.route('/send', methods=['POST'])
def send_message_legacy():
    """Envia mensagem (compatibilidade)"""
    try:
        data = request.get_json()
        phone = data.get("phone")
        message = data.get("message")
        
        if not phone or not message:
            return jsonify({"error": "phone and message are required"}), 400
        
        # Usa primeira conta disponível
        accounts = account_manager.get_all_accounts()
        if not accounts:
            return jsonify({"error": "Nenhuma conta configurada"}), 400
        
        account_id = accounts[0]['id']
        success = instance_manager.send_message(account_id, phone, message)
        return jsonify({"success": success}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5002))
    print(f"\n🚀 Ylada BOT Multi-Instance rodando em http://localhost:{port}")
    print(f"📖 Dashboard: http://localhost:{port}")
    print(f"💡 Suporta múltiplas instâncias WhatsApp")
    print(f"📚 Configure suas contas com: python scripts/init_4_accounts.py\n")
    app.run(host='0.0.0.0', port=port, debug=True)

