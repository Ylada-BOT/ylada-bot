"""
API Flask Simplificada - Ylada BOT
Apenas o essencial para uso imediato

NOTA: Versão completa disponível em app_completo.py (como referência)
Esta versão contém apenas o que você vai usar agora.
Conforme for precisando, adicione funcionalidades gradualmente.
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

from bot_simple import LadaBotSimple
from whatsapp_webjs_handler import WhatsAppWebJSHandler
from users_manager import UsersManager
from campaigns_manager import CampaignsManager

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
CORS(app)

# Inicializa bot simplificado (com tratamento de erro)
try:
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    # Verifica se o arquivo existe, senão usa None (bot cria config padrão)
    if not os.path.exists(config_path):
        config_path = None
    bot = LadaBotSimple(config_path=config_path)
except Exception as e:
    print(f"[!] Erro ao inicializar bot: {e}")
    bot = None

# Handler WhatsApp Web.js (opcional - para conversas reais)
try:
    whatsapp_webjs = WhatsAppWebJSHandler(instance_name="ylada_bot", port=5001)
except Exception as e:
    print(f"[!] Erro ao inicializar WhatsApp handler: {e}")
    whatsapp_webjs = None

# Gerenciadores adicionais (estilo Botconversa)
try:
    users_manager = UsersManager()
    campaigns_manager = CampaignsManager()
except Exception as e:
    print(f"[!] Erro ao inicializar gerenciadores: {e}")
    users_manager = None
    campaigns_manager = None


@app.route('/', methods=['GET'])
def index():
    """Dashboard principal - Versão simplificada"""
    return render_template('index_simple.html')


@app.route('/health', methods=['GET'])
def health():
    """Status do servidor"""
    return jsonify({"status": "ok", "bot": "Ylada BOT"})


@app.route('/send', methods=['POST'])
def send_message():
    """Envia mensagem"""
    try:
        if not bot:
            return jsonify({"error": "Bot não inicializado"}), 500
        
        data = request.get_json()
        phone = data.get("phone")
        message = data.get("message")
        
        if not phone or not message:
            return jsonify({"error": "phone and message are required"}), 400
        
        success = bot.send_message(phone, message)
        return jsonify({"success": success}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/webhook', methods=['POST'])
def webhook():
    """Recebe mensagens via webhook"""
    try:
        if not bot:
            return jsonify({"error": "Bot não inicializado"}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data"}), 400
        
        response = bot.handle_webhook(data)
        return jsonify({"status": "processed", "response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/qr', methods=['GET'])
def qr_code_page():
    """Página para conectar WhatsApp"""
    # Em produção, o servidor está no Render, não precisa iniciar localmente
    if os.getenv('ENVIRONMENT') != 'production' and whatsapp_webjs:
        # Apenas em desenvolvimento tenta iniciar servidor local
        try:
            import requests
            try:
                requests.get("http://localhost:5001/health", timeout=1)
            except:
                # Servidor não está rodando, inicia
                print("[*] Iniciando servidor WhatsApp Web.js ao acessar /qr...")
                whatsapp_webjs.start_server()
        except Exception as e:
            print(f"[!] Erro ao verificar/iniciar servidor: {e}")
    
    return render_template('qr_code.html')


@app.route('/api/qr', methods=['GET'])
def get_qr():
    """Retorna QR Code do WhatsApp Web.js"""
    try:
        import requests
        
        # URL do servidor WhatsApp (Render em produção, localhost em desenvolvimento)
        whatsapp_server_url = os.getenv('WHATSAPP_SERVER_URL', 'http://localhost:5001')
        
        # Se estiver em produção e não tiver URL configurada, usa Render padrão
        if os.getenv('ENVIRONMENT') == 'production' and whatsapp_server_url == 'http://localhost:5001':
            whatsapp_server_url = os.getenv('RENDER_WHATSAPP_URL', 'https://ylada-bot.onrender.com')
        
        # Busca QR Code diretamente do servidor Render
        try:
            response = requests.get(f"{whatsapp_server_url}/qr", timeout=5)
            if response.status_code == 200:
                data = response.json()
                ready_status = data.get("ready", False)
                
                # Verificação adicional: se diz que está ready, tenta confirmar buscando chats
                if ready_status:
                    try:
                        chats_check = requests.get(f"{whatsapp_server_url}/chats", timeout=3)
                        if chats_check.status_code != 200:
                            # Se não conseguiu buscar chats, não está realmente conectado
                            ready_status = False
                    except:
                        # Se deu erro, não está conectado
                        ready_status = False
                
                return jsonify({
                    "ready": ready_status,
                    "qr": data.get("qr") if not ready_status else None,
                    "message": "WhatsApp conectado!" if ready_status else "Escaneie o QR Code para conectar"
                }), 200
        except requests.exceptions.RequestException as e:
            # Se não conseguir conectar, tenta método local (desenvolvimento)
            if whatsapp_server_url == 'http://localhost:5001' and whatsapp_webjs:
                # Verifica se já está conectado localmente
                if whatsapp_webjs.is_ready():
                    return jsonify({
                        "ready": True,
                        "qr": None,
                        "message": "WhatsApp já conectado!"
                    }), 200
                
                # Tenta iniciar servidor local
                try:
                    health_check = requests.get("http://localhost:5001/health", timeout=2)
                    if health_check.status_code == 200:
                        qr = whatsapp_webjs.get_qr_code()
                        if qr:
                            return jsonify({
                                "ready": False,
                                "qr": qr,
                                "message": "Escaneie o QR Code para conectar"
                            }), 200
                except:
                    pass
                
                # Inicia servidor local se não estiver rodando
                if whatsapp_webjs.start_server():
                    time.sleep(5)
                    qr = whatsapp_webjs.get_qr_code()
                    if qr:
                        return jsonify({
                            "ready": False,
                            "qr": qr,
                            "message": "Servidor iniciado! Escaneie o QR Code abaixo"
                        }), 200
            
            return jsonify({
                "ready": False,
                "qr": None,
                "error": f"Não foi possível conectar ao servidor WhatsApp. URL: {whatsapp_server_url}",
                "message": "Acesse os logs do Render para ver o QR Code: https://dashboard.render.com"
            }), 503
            
    except Exception as e:
        print(f"[!] Erro ao obter QR Code: {e}")
        return jsonify({
            "ready": False,
            "qr": None,
            "error": str(e),
            "message": "Acesse os logs do Render para ver o QR Code: https://dashboard.render.com"
        }), 500


@app.route('/api/whatsapp-status', methods=['GET'])
def whatsapp_status():
    """Status da conexão WhatsApp - verificação robusta"""
    if not whatsapp_webjs:
        return jsonify({
            "ready": False,
            "mode": "simple",
            "message": "WhatsApp handler não inicializado",
            "connected": False
        }), 200
    
    # Verifica status básico
    try:
        import requests
        status_response = requests.get(f"{whatsapp_webjs.base_url}/status", timeout=2)
        status_data = status_response.json()
        basic_ready = status_data.get("ready", False)
        actually_connected = status_data.get("actuallyConnected", False)
    except:
        basic_ready = False
        actually_connected = False
    
    # Verificação mais robusta
    is_ready = whatsapp_webjs.is_ready()
    
    # Se a verificação robusta diz que não está pronto, usa esse resultado
    final_ready = is_ready and (actually_connected if actually_connected is not None else basic_ready)
    
    return jsonify({
        "ready": final_ready,
        "mode": "webjs" if final_ready else "simple",
        "message": "WhatsApp conectado!" if final_ready else "Aguardando conexão...",
        "connected": final_ready,
        "basic_status": basic_ready,
        "actually_connected": actually_connected
    }), 200


@app.route('/api/restart-server', methods=['POST'])
def restart_server():
    """Reinicia o servidor Node.js"""
    try:
        if not whatsapp_webjs:
            return jsonify({"success": False, "error": "WhatsApp handler não inicializado"}), 500
        
        whatsapp_webjs.stop_server()
        time.sleep(2)
        whatsapp_webjs.start_server()
        return jsonify({"success": True, "message": "Servidor reiniciado"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ========== FUNCIONALIDADES ESTILO BOTCONVERSA ==========

@app.route('/api/users', methods=['GET', 'POST'])
def manage_users():
    """Gerencia usuários/atendentes"""
    if request.method == 'GET':
        role = request.args.get('role')
        users = users_manager.list_users(role=role)
        return jsonify({"users": users, "total": len(users)}), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        user = users_manager.create_user(
            username=data.get("username"),
            email=data.get("email"),
            role=data.get("role", "attendant")
        )
        return jsonify({"success": True, "user": user}), 201


@app.route('/api/campaigns', methods=['GET', 'POST'])
def manage_campaigns():
    """Gerencia campanhas com QR Code"""
    if not campaigns_manager:
        return jsonify({"campaigns": [], "total": 0, "error": "Campaigns manager não inicializado"}), 200
    
    if request.method == 'GET':
        active_only = request.args.get('active_only', 'false').lower() == 'true'
        campaigns = campaigns_manager.list_campaigns(active_only=active_only)
        return jsonify({"campaigns": campaigns, "total": len(campaigns)}), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        campaign = campaigns_manager.create_campaign(
            name=data.get("name"),
            message=data.get("message"),
            flow_name=data.get("flow_name")
        )
        return jsonify({"success": True, "campaign": campaign}), 201


@app.route('/campaigns', methods=['GET'])
def campaigns_page():
    """Página de campanhas"""
    return render_template('campaigns.html')


@app.route('/broadcast', methods=['GET'])
def broadcast_page():
    """Página de transmissão"""
    return render_template('broadcast.html')


@app.route('/live-chat', methods=['GET'])
def live_chat_page():
    """Página de bate-papo ao vivo"""
    return render_template('live_chat.html')


@app.route('/automation', methods=['GET'])
def automation_page():
    """Página de automação"""
    return render_template('automation.html')


@app.route('/settings', methods=['GET'])
def settings_page():
    """Página de configurações"""
    return render_template('settings.html')


@app.route('/flow-builder', methods=['GET'])
def flow_builder():
    """Página do construtor visual de fluxos"""
    return render_template('flow_builder.html')


@app.route('/api/flows', methods=['GET', 'POST'])
def manage_flows():
    """Gerencia fluxos de conversa"""
    if request.method == 'GET':
        # Lista todos os fluxos
        flows_dir = Path("data/flows")
        flows_dir.mkdir(parents=True, exist_ok=True)
        
        flows = []
        for flow_file in flows_dir.glob("*.json"):
            try:
                with open(flow_file, "r", encoding="utf-8") as f:
                    flow_data = json.load(f)
                    flows.append({
                        "name": flow_data.get("name"),
                        "nodes_count": len(flow_data.get("nodes", [])),
                        "created_at": flow_data.get("created_at")
                    })
            except:
                pass
        
        return jsonify({"flows": flows, "total": len(flows)}), 200
    
    elif request.method == 'POST':
        # Salva novo fluxo
        data = request.get_json()
        flow_name = data.get("name", "unnamed")
        
        flows_dir = Path("data/flows")
        flows_dir.mkdir(parents=True, exist_ok=True)
        
        flow_file = flows_dir / f"{flow_name.replace(' ', '_')}.json"
        with open(flow_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Opcional: Converte e importa para config.yaml automaticamente
        import_auto = request.args.get('import', 'false').lower() == 'true'
        if import_auto:
            try:
                from flow_converter import FlowConverter
                yaml_flow = FlowConverter.visual_to_yaml(data)
                FlowConverter.save_to_config(
                    flow_name.lower().replace(" ", "_"),
                    yaml_flow,
                    os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
                )
            except Exception as e:
                print(f"[!] Erro ao importar fluxo: {e}")
        
        return jsonify({"success": True, "message": "Fluxo salvo com sucesso"}), 201


@app.route('/api/keywords', methods=['GET'])
def get_keywords():
    """Lista palavras-chave do config"""
    try:
        import yaml
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        
        keywords_config = config.get("keywords", {})
        keywords = []
        
        for keyword, response in keywords_config.items():
            keywords.append({
                "name": keyword,
                "keywords": [keyword],
                "type": "contains",
                "response": response,
                "executions": 0,
                "active": True
            })
        
        return jsonify({"keywords": keywords, "total": len(keywords)}), 200
    except Exception as e:
        return jsonify({"keywords": [], "total": 0, "error": str(e)}), 200


@app.route('/api/flows/<flow_name>', methods=['GET', 'DELETE'])
def get_flow(flow_name):
    """Obtém ou deleta um fluxo específico"""
    flows_dir = Path("data/flows")
    flow_file = flows_dir / f"{flow_name.replace(' ', '_')}.json"
    
    if request.method == 'GET':
        if flow_file.exists():
            with open(flow_file, "r", encoding="utf-8") as f:
                flow_data = json.load(f)
            return jsonify({"flow": flow_data}), 200
        else:
            return jsonify({"error": "Fluxo não encontrado"}), 404
    
    elif request.method == 'DELETE':
        if flow_file.exists():
            flow_file.unlink()
            return jsonify({"success": True, "message": "Fluxo deletado"}), 200
        else:
            return jsonify({"error": "Fluxo não encontrado"}), 404


@app.route('/campaign/<campaign_id>', methods=['GET'])
def campaign_redirect(campaign_id):
    """Redireciona campanha e aciona fluxo"""
    if not campaigns_manager:
        return jsonify({"error": "Campaigns manager não inicializado"}), 500
    
    campaign = campaigns_manager.get_campaign(campaign_id)
    if not campaign:
        return jsonify({"error": "Campanha não encontrada"}), 404
    
    campaigns_manager.track_click(campaign_id)
    
    # Retorna página HTML com redirecionamento para WhatsApp
    phone = request.args.get('phone', '')
    message = campaign.get("message", "")
    flow_name = campaign.get("flow_name")
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Redirecionando...</title>
        <meta http-equiv="refresh" content="2;url=https://wa.me/{phone}?text={message}">
    </head>
    <body>
        <h1>Redirecionando para WhatsApp...</h1>
        <p>Se não redirecionar automaticamente, <a href="https://wa.me/{phone}?text={message}">clique aqui</a></p>
    </body>
    </html>
    """


@app.route('/contacts', methods=['GET'])
def contacts_page():
    """Página de audiência/contatos"""
    # Se for requisição HTML, retorna página
    if 'text/html' in request.headers.get('Accept', ''):
        return render_template('contacts.html')
    
    # Se for JSON (API), retorna dados
    return get_contacts_data()


@app.route('/api/sync-contacts', methods=['POST'])
def sync_contacts():
    """Sincroniza contatos do WhatsApp e salva no banco"""
    try:
        if not whatsapp_webjs or not whatsapp_webjs.is_ready():
            return jsonify({
                "success": False,
                "error": "WhatsApp não está conectado. Conecte primeiro em /qr"
            }), 400
        
        # Busca contatos do WhatsApp
        whatsapp_chats = whatsapp_webjs.get_chats()
        
        # Filtra apenas contatos individuais (não grupos)
        contacts_to_sync = []
        for chat in whatsapp_chats:
            if not chat.get('isGroup', False):
                phone = chat.get('phone', '')
                if phone:
                    # Remove caracteres não numéricos e formata
                    phone_clean = ''.join(filter(str.isdigit, phone))
                    if len(phone_clean) >= 10:  # Telefone válido
                        contacts_to_sync.append({
                            'phone': phone_clean,
                            'name': chat.get('name', 'Sem nome'),
                            'source': 'whatsapp'
                        })
        
        # Salva no banco de dados (usando account_id padrão para uso pessoal)
        # Por enquanto, usa account_id fixo "owner" ou cria uma conta padrão
        try:
            from database import Database
            db = Database(use_sqlite=True)  # Usa SQLite local por enquanto
            
            # Busca ou cria conta padrão
            default_account = db.get_account_by_phone("owner")
            if not default_account:
                default_account = db.create_account({
                    'name': 'Conta Principal',
                    'phone': 'owner',
                    'plan': 'owner',
                    'status': 'active'
                })
            
            account_id = default_account['id']
        except Exception as e:
            print(f"[!] Erro ao acessar banco de dados: {e}")
            # Se não conseguir usar banco, retorna apenas contagem
            return jsonify({
                "success": True,
                "total_contacts": len(contacts_to_sync),
                "synced": 0,
                "updated": 0,
                "message": f"Encontrados {len(contacts_to_sync)} contatos, mas não foi possível salvar no banco",
                "warning": "Banco de dados não disponível. Contatos não foram salvos."
            }), 200
        
        # Salva/atualiza contatos
        synced_count = 0
        updated_count = 0
        for contact_data in contacts_to_sync:
            # Verifica se já existe
            existing = db.get_contact_by_phone(account_id, contact_data['phone'])
            
            if existing:
                # Atualiza nome se mudou
                if existing.get('name') != contact_data['name']:
                    db.update_contact(existing['id'], {'name': contact_data['name']})
                    updated_count += 1
            else:
                # Cria novo contato
                db.create_contact({
                    'account_id': account_id,
                    'phone': contact_data['phone'],
                    'name': contact_data['name'],
                    'tags': []
                })
                synced_count += 1
        
        return jsonify({
            "success": True,
            "total_contacts": len(contacts_to_sync),
            "synced": synced_count,
            "updated": updated_count,
            "message": f"Sincronizados {synced_count} novos contatos e atualizados {updated_count} existentes"
        }), 200
        
    except Exception as e:
        print(f"[!] Erro ao sincronizar contatos: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


def get_contacts_data():
    """Lista contatos - combina dados do bot com WhatsApp"""
    search = request.args.get('search', '')
    
    # Busca contatos do bot
    bot_contacts = bot.contacts.list_contacts(search=search if search else None)
    stats = bot.contacts.get_stats()
    
    # Busca contatos reais do WhatsApp
    whatsapp_contacts = []
    try:
        if whatsapp_webjs and whatsapp_webjs.is_ready():
            whatsapp_chats = whatsapp_webjs.get_chats()
            # Converte chats em contatos
            for chat in whatsapp_chats:
                if not chat.get('isGroup', False):  # Apenas contatos individuais
                    whatsapp_contacts.append({
                        'phone': chat.get('phone', ''),
                        'name': chat.get('name', 'Sem nome'),
                        'id': chat.get('id', ''),
                        'last_message': chat.get('lastMessage', ''),
                        'last_message_time': chat.get('timestamp', 0),
                        'unread_count': chat.get('unreadCount', 0),
                        'source': 'whatsapp'
                    })
    except Exception as e:
        print(f"[!] Erro ao buscar contatos do WhatsApp: {e}")
    
    # Combina contatos (prioriza WhatsApp, depois bot)
    all_contacts = {}
    for contact in whatsapp_contacts:
        phone = contact['phone']
        if phone:
            all_contacts[phone] = contact
    
    # Adiciona contatos do bot que não estão no WhatsApp
    for contact in bot_contacts:
        phone = contact.get('phone', '')
        if phone and phone not in all_contacts:
            contact['source'] = 'bot'
            all_contacts[phone] = contact
    
    # Converte para lista
    contacts_list = list(all_contacts.values())
    
    # Aplica busca se necessário
    if search:
        search_lower = search.lower()
        contacts_list = [
            c for c in contacts_list
            if search_lower in c.get('name', '').lower() or search_lower in c.get('phone', '')
        ]
    
    # Atualiza stats com dados do WhatsApp
    stats['total_contacts'] = len(contacts_list)
    stats['whatsapp_contacts'] = len(whatsapp_contacts)
    
    return jsonify({
        "contacts": contacts_list,
        "stats": stats,
        "total": len(contacts_list)
    }), 200




@app.route('/conversations', methods=['GET'])
def get_conversations():
    """Lista conversas"""
    if not bot:
        return jsonify({
            "conversations": {},
            "messages_log": [],
            "whatsapp_chats": [],
            "has_real_chats": False
        }), 200
    
    conversations = bot.conversation.conversations
    messages_log = bot.whatsapp.get_messages_log()
    
    # Tenta buscar conversas reais do WhatsApp Web.js
    whatsapp_chats = []
    try:
        if whatsapp_webjs:
            # Verifica se o servidor está rodando
            if not whatsapp_webjs.is_ready():
                # Tenta iniciar o servidor se não estiver rodando
                try:
                    import requests
                    requests.get(f"http://localhost:5001/health", timeout=1)
                except:
                    # Servidor não está rodando, tenta iniciar
                    print("[*] Tentando iniciar servidor WhatsApp Web.js...")
                    whatsapp_webjs.start_server()
                    time.sleep(3)
            
            # Se estiver pronto, busca chats
            if whatsapp_webjs.is_ready():
                whatsapp_chats = whatsapp_webjs.get_chats()
    except Exception as e:
        print(f"[!] Erro ao buscar chats reais: {e}")
    
    return jsonify({
        "conversations": conversations,
        "messages_log": messages_log,
        "whatsapp_chats": whatsapp_chats,  # Conversas reais do WhatsApp
        "has_real_chats": len(whatsapp_chats) > 0
    }), 200


@app.route('/api/chats/<chat_id>/messages', methods=['GET'])
def get_chat_messages(chat_id):
    """Busca mensagens de um chat específico"""
    try:
        if not whatsapp_webjs:
            return jsonify({
                "success": False,
                "error": "WhatsApp handler não inicializado",
                "messages": []
            }), 500
        
        limit = request.args.get('limit', 50, type=int)
        messages = whatsapp_webjs.get_chat_messages(chat_id, limit)
        return jsonify({
            "success": True,
            "messages": messages,
            "total": len(messages)
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "messages": []
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5002))  # Porta 5002 (5000 ocupada pelo AirPlay no macOS)
    print(f"\n🚀 Ylada BOT rodando em http://localhost:{port}")
    print(f"📖 Dashboard: http://localhost:{port}")
    print(f"💡 Versão simplificada - Apenas o essencial")
    print(f"📚 Versão completa disponível em: app_completo.py\n")
    app.run(host='0.0.0.0', port=port, debug=True)

