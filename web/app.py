"""
BOT by YLADA
Integração WhatsApp + Inteligência Artificial

Simples: Conecte WhatsApp, configure IA, receba respostas automáticas.
"""
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from whatsapp_webjs_handler import WhatsAppWebJSHandler
from ai_handler import AIHandler

# Cria o app PRIMEIRO
app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'),
            static_url_path='/static')
CORS(app)

# Configuração de sessão
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuração de autenticação
# Defina AUTH_REQUIRED=true para ativar autenticação (produção)
# Por padrão, desabilitado para facilitar desenvolvimento
AUTH_REQUIRED = os.getenv('AUTH_REQUIRED', 'false').lower() == 'true'

# Decorator para proteger rotas (requer login)
def require_login(f):
    """Decorator para exigir autenticação nas rotas de páginas"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Se autenticação está desabilitada, permite acesso
        if not AUTH_REQUIRED:
            return f(*args, **kwargs)
        
        # Verifica se usuário está logado
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        
        return f(*args, **kwargs)
    
    return decorated_function

# Decorator para proteger APIs (requer login)
def require_api_auth(f):
    """Decorator para exigir autenticação nas rotas de API"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Se autenticação está desabilitada, permite acesso
        if not AUTH_REQUIRED:
            return f(*args, **kwargs)
        
        # Verifica se usuário está logado
        if 'user_id' not in session:
            return jsonify({'error': 'Não autenticado. Faça login primeiro.'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

# Importa rotas de autenticação (pode falhar se DB não estiver configurado)
try:
    from web.api.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
except Exception as e:
    print(f"[!] Rotas de autenticação não disponíveis: {e}")
    print("[!] Configure o banco de dados para usar autenticação completa")

# Importa rotas de fluxos
try:
    from web.api.flows import bp as flows_bp
    app.register_blueprint(flows_bp)
    print("[✓] Rotas de fluxos registradas")
except Exception as e:
    print(f"[!] Rotas de fluxos não disponíveis: {e}")

# Importa rotas de notificações
try:
    from web.api.notifications import bp as notifications_bp
    app.register_blueprint(notifications_bp)
    print("[✓] Rotas de notificações registradas")
except Exception as e:
    print(f"[!] Rotas de notificações não disponíveis: {e}")

# Importa rotas de leads
try:
    from web.api.leads import bp as leads_bp
    app.register_blueprint(leads_bp)
    print("[✓] Rotas de leads registradas")
except Exception as e:
    print(f"[!] Rotas de leads não disponíveis: {e}")

# Importa rotas de tenants
try:
    from web.api.tenants import bp as tenants_bp
    app.register_blueprint(tenants_bp)
    print("[✓] Rotas de tenants registradas")
except Exception as e:
    print(f"[!] Rotas de tenants não disponíveis: {e}")

# Importa rotas de instâncias
try:
    from web.api.instances import bp as instances_bp
    app.register_blueprint(instances_bp)
    print("[✓] Rotas de instâncias registradas")
except Exception as e:
    print(f"[!] Rotas de instâncias não disponíveis: {e}")

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
# CARREGAR FLUXOS DO BANCO DE DADOS
# ============================================
def load_flows_on_startup():
    """Carrega fluxos ativos do banco ou arquivo ao iniciar"""
    try:
        from src.flows.flow_loader import load_active_flows_from_db
        count = load_active_flows_from_db()
        if count > 0:
            print(f"[✓] {count} fluxo(s) carregado(s) do banco de dados")
        else:
            print("[!] Nenhum fluxo ativo encontrado no banco")
            # Tenta carregar de arquivo JSON
            try:
                import json
                import os
                flows_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'flows_memory.json')
                if os.path.exists(flows_file):
                    with open(flows_file, 'r') as f:
                        flows_data = json.load(f)
                    from src.flows.flow_engine import flow_engine
                    loaded = 0
                    for flow in flows_data.get('flows', []):
                        if flow.get('status') == 'active':
                            flow_data = flow.get('flow_data', {})
                            if flow_data:
                                success = flow_engine.load_flow(flow['id'], flow_data)
                                if success:
                                    loaded += 1
                                    print(f"[✓] Fluxo carregado do arquivo: {flow.get('name')} (ID: {flow['id']})")
                    if loaded > 0:
                        print(f"[✓] Total: {loaded} fluxo(s) carregado(s) do arquivo")
            except Exception as file_error:
                print(f"[!] Erro ao carregar fluxos do arquivo: {file_error}")
    except Exception as e:
        print(f"[!] Erro ao carregar fluxos do banco: {e}")
        # Tenta carregar de arquivo JSON
        try:
            import json
            import os
            flows_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'flows_memory.json')
            if os.path.exists(flows_file):
                with open(flows_file, 'r') as f:
                    flows_data = json.load(f)
                from src.flows.flow_engine import flow_engine
                loaded = 0
                for flow in flows_data.get('flows', []):
                    if flow.get('status') == 'active':
                        success = flow_engine.load_flow(flow['id'], flow.get('flow_data', {}))
                        if success:
                            loaded += 1
                if loaded > 0:
                    print(f"[✓] {loaded} fluxo(s) carregado(s) do arquivo")
        except Exception as file_error:
            print(f"[!] Erro ao carregar fluxos do arquivo: {file_error}")
        print("[!] Sistema funcionará apenas com fluxos criados em memória")

# Carrega fluxos ao iniciar
load_flows_on_startup()

# ============================================
# ROTAS - AUTENTICAÇÃO (PÁGINAS)
# ============================================

@app.route('/login')
def login_page():
    """Página de login"""
    return render_template('auth/login.html')

@app.route('/register')
def register_page():
    """Página de registro"""
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    return redirect(url_for('login_page'))

# ============================================
# ROTAS - DASHBOARD
# ============================================

@app.route('/')
@require_login
def index():
    """Dashboard principal"""
    config = load_config()
    
    # Verifica status do WhatsApp - SEMPRE começa como desconectado
    # O status será verificado via JavaScript em tempo real
    # Isso evita mostrar "Conectado" quando não está
    # Usa novo template com sidebar
    try:
        return render_template('dashboard_new.html')
    except:
        # Fallback para template antigo se novo não existir
        return render_template('dashboard.html')

@app.route('/simple')
def index_simple():
    """Dashboard simples (sem tenants) - Modo desenvolvimento"""
    config = load_config()
    return render_template('dashboard.html')

@app.route('/flows')
@require_login
def flows_list():
    """Lista de fluxos"""
    return render_template('flows/list.html')

@app.route('/flows/new')
@require_login
def flows_new():
    """Criar novo fluxo"""
    return render_template('flows/new.html')

@app.route('/notifications')
@require_login
def notifications_list():
    """Lista de notificações"""
    return render_template('notifications/list.html')

@app.route('/leads')
@require_login
def leads_list():
    """Lista de leads"""
    return render_template('leads/list.html')

@app.route('/conversations')
@require_login
def conversations_list():
    """Lista de conversas"""
    return render_template('conversations/list.html')

# ============================================
# ROTAS - TENANTS
# ============================================

@app.route('/tenants')
@require_login
def tenants_list():
    """Lista de tenants"""
    return render_template('tenants/list.html')

@app.route('/tenants/new')
@require_login
def tenants_new():
    """Criar novo tenant"""
    return render_template('tenants/create.html')

@app.route('/tenants/<int:tenant_id>')
@require_login
def tenants_detail(tenant_id):
    """Detalhes do tenant"""
    return render_template('tenants/dashboard.html', tenant_id=tenant_id)

# ============================================
# ROTAS - INSTÂNCIAS
# ============================================

@app.route('/instances')
@require_login
def instances_list():
    """Lista de instâncias"""
    tenant_id = request.args.get('tenant_id', type=int)
    return render_template('instances/list.html', tenant_id=tenant_id)

@app.route('/instances/new')
@require_login
def instances_new():
    """Criar nova instância"""
    tenant_id = request.args.get('tenant_id', type=int)
    return render_template('instances/create.html', tenant_id=tenant_id)

@app.route('/instances/<int:instance_id>')
@require_login
def instances_detail(instance_id):
    """Detalhes da instância"""
    return render_template('instances/dashboard.html', instance_id=instance_id)

@app.route('/instances/<int:instance_id>/connect')
@require_login
def instances_connect(instance_id):
    """Conectar WhatsApp da instância"""
    return render_template('instances/connect.html', instance_id=instance_id)

# ============================================
# ROTAS - WHATSAPP
# ============================================

@app.route('/qr')
@require_login
def qr_code():
    """Página para escanear QR Code"""
    return render_template('qr.html')

@app.route('/api/qr')
def get_qr():
    """Obtém QR Code do WhatsApp"""
    if not whatsapp:
        return jsonify({"error": "WhatsApp não inicializado"}), 500
    
    try:
        # Verifica status detalhado primeiro
        import requests
        try:
            status_response = requests.get(f"http://localhost:{whatsapp.port}/status", timeout=2)
            if status_response.status_code == 200:
                status_data = status_response.json()
                has_qr = status_data.get("hasQr", False)
                actually_connected = status_data.get("actuallyConnected", False)
                
                # Se realmente está conectado, retorna connected
                if actually_connected:
                    return jsonify({"status": "connected"})
                
                # Se tem QR code, retorna o QR
                if has_qr:
                    qr_data = whatsapp.get_qr_code()
                    if qr_data:
                        return jsonify({"qr": qr_data, "status": "waiting"})
        except:
            pass
        
        # Tenta obter QR code
        qr_data = whatsapp.get_qr_code()
        if qr_data:
            return jsonify({"qr": qr_data, "status": "waiting"})
        else:
            # Verifica se realmente está conectado (verificação dupla)
            if whatsapp.is_ready():
                # Verifica novamente com status detalhado
                try:
                    status_response = requests.get(f"http://localhost:{whatsapp.port}/status", timeout=2)
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        if status_data.get("actuallyConnected", False):
                            return jsonify({"status": "connected"})
                except:
                    pass
            
            return jsonify({"status": "generating"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/conversations')
@require_api_auth
def get_conversations():
    """Obtém lista de conversas do WhatsApp"""
    if not whatsapp:
        return jsonify({"success": False, "error": "WhatsApp não inicializado"}), 500
    
    try:
        import requests
        whatsapp_port = whatsapp.port if hasattr(whatsapp, 'port') else 5001
        response = requests.get(f"http://localhost:{whatsapp_port}/chats", timeout=10)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"success": False, "error": "Erro ao buscar conversas"}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": f"Servidor WhatsApp não está respondendo: {str(e)}"}), 503
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/conversations/<chat_id>/messages')
@require_api_auth
def get_conversation_messages(chat_id):
    """Obtém mensagens de uma conversa específica"""
    if not whatsapp:
        return jsonify({"success": False, "error": "WhatsApp não inicializado"}), 500
    
    try:
        import requests
        limit = request.args.get('limit', 50, type=int)
        response = requests.get(
            f"http://localhost:{whatsapp.port}/chats/{chat_id}/messages",
            params={"limit": limit},
            timeout=10
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"success": False, "error": "Erro ao buscar mensagens"}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": f"Servidor WhatsApp não está respondendo: {str(e)}"}), 503
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/whatsapp-status')
def whatsapp_status():
    """Status da conexão WhatsApp"""
    if not whatsapp:
        return jsonify({"connected": False, "error": "WhatsApp não inicializado"})
    
    try:
        # Verifica se o servidor Node.js está rodando
        import requests
        try:
            whatsapp_port = whatsapp.port if hasattr(whatsapp, 'port') else 5001
            server_response = requests.get(f"http://localhost:{whatsapp_port}/health", timeout=2)
            if server_response.status_code != 200:
                return jsonify({"connected": False, "error": "Servidor WhatsApp não está respondendo"})
        except requests.exceptions.RequestException:
            return jsonify({"connected": False, "error": "Servidor WhatsApp não está rodando", "hasQr": False})
        
        # Verifica status detalhado
        try:
            whatsapp_port = whatsapp.port if hasattr(whatsapp, 'port') else 5001
            status_response = requests.get(f"http://localhost:{whatsapp_port}/status", timeout=2)
            if status_response.status_code == 200:
                status_data = status_response.json()
                has_qr = status_data.get("hasQr", False)
                actually_connected = status_data.get("actuallyConnected", False)
                ready = status_data.get("ready", False)
                
                # Só considera conectado se realmente estiver conectado (não apenas se o servidor está rodando)
                connected = actually_connected or (ready and not has_qr)
                
                if connected:
                    return jsonify({
                        "connected": True, 
                        "message": "WhatsApp conectado",
                        "hasQr": False
                    })
                elif has_qr:
                    return jsonify({
                        "connected": False, 
                        "message": "QR Code disponível. Escaneie para conectar.",
                        "hasQr": True
                    })
                else:
                    return jsonify({
                        "connected": False, 
                        "message": "Aguardando conexão. Clique em 'Conectar WhatsApp' para gerar QR Code.",
                        "hasQr": False
                    })
        except requests.exceptions.RequestException:
            pass
        
        # Fallback: verifica se realmente está conectado
        connected = whatsapp.is_ready()
        
        if connected:
            return jsonify({"connected": True, "message": "WhatsApp conectado", "hasQr": False})
        else:
            return jsonify({"connected": False, "message": "Aguardando conexão. Escaneie o QR Code.", "hasQr": False})
            
    except Exception as e:
        return jsonify({"connected": False, "error": str(e), "hasQr": False})

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
@require_api_auth
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
    Processa com fluxos de automação e/ou IA
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
        
        # Tenta processar com fluxos primeiro
        try:
            from src.whatsapp.message_handler import message_handler
            
            # Processa mensagem com fluxos
            flow_result = message_handler.process_message(
                phone=phone,
                message=message,
                whatsapp_handler=whatsapp
            )
            
            if flow_result.get('processed') and flow_result.get('flows_executed'):
                print(f"[🔄] Fluxos executados: {len(flow_result['flows_executed'])}")
                
                # Verifica se alguma mensagem foi enviada
                flows_with_messages = [
                    f for f in flow_result.get('flows_executed', [])
                    if f.get('result', {}).get('success')
                ]
                
                if flows_with_messages:
                    print(f"[✓] {len(flows_with_messages)} fluxo(s) executado(s) com sucesso")
                else:
                    print(f"[!] Fluxos executados mas nenhuma mensagem foi enviada")
                
                return jsonify({
                    "success": True,
                    "processed_by": "flows",
                    "flows_executed": flow_result['flows_executed'],
                    "messages_sent": len(flows_with_messages)
                })
            
        except ImportError:
            # Fluxos não disponíveis ainda, continua com IA
            print("[!] Sistema de fluxos não disponível, usando IA")
        except Exception as e:
            print(f"[!] Erro ao processar com fluxos: {e}")
            # Continua com IA como fallback
        
        # Fallback: Processa com IA (se fluxos não processaram)
        config = load_config()
        if not config.get('api_key'):
            print("[!] IA não configurada. Configure no dashboard primeiro.")
            return jsonify({
                "success": False,
                "error": "IA não configurada e nenhum fluxo ativo"
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
            "processed_by": "ai",
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

