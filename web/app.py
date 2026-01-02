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

# Rate limiting
from web.utils.rate_limiter import init_rate_limiter, rate_limit_whatsapp, limiter
from config.settings import REDIS_URL, USE_REDIS

# Fila de mensagens
from web.utils.message_queue import init_message_queue, get_message_queue
from web.workers.message_worker import init_message_worker, get_message_worker
import threading

# Cria o app PRIMEIRO
app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'),
            static_url_path='/static')
CORS(app)

# Handler global para erros não tratados - sempre retorna JSON para APIs
from werkzeug.exceptions import HTTPException

@app.errorhandler(HTTPException)
def handle_http_error(e):
    """Handler para erros HTTP - retorna JSON para APIs"""
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'error': e.name,
            'message': e.description
        }), e.code
    return e

@app.errorhandler(Exception)
def handle_generic_error(e):
    """Handler para erros genéricos não tratados - retorna JSON para APIs"""
    # Se a rota é uma API, retorna JSON
    if request.path.startswith('/api/'):
        import traceback
        error_msg = str(e)
        
        # Erros de banco de dados
        if 'psycopg2' in error_msg or 'OperationalError' in error_msg or 'connection' in error_msg.lower() or 'Tenant or user not found' in error_msg:
            return jsonify({
                'success': False,
                'error': 'Erro de conexão com o banco de dados',
                'message': 'Verifique se a DATABASE_URL está correta no arquivo .env.local',
                'hint': 'Acesse: Settings > Database no Supabase para obter a connection string correta',
                'details': error_msg if app.debug else None
            }), 503
        
        # Outros erros
        logger.error(f"Erro não tratado em {request.path}: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor',
            'message': error_msg if app.debug else 'Ocorreu um erro. Tente novamente.',
            'details': traceback.format_exc() if app.debug else None
        }), 500
    
    # Para rotas não-API, deixa o Flask tratar normalmente
    raise e

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

# Decorator para exigir role de admin
def require_admin(f):
    """Decorator para exigir que o usuário seja admin"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Se autenticação está desabilitada, permite acesso
        if not AUTH_REQUIRED:
            return f(*args, **kwargs)
        
        # Verifica se usuário está logado
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        
        # Verifica se é admin
        user_role = session.get('user_role', 'user')
        if user_role != 'admin':
            return redirect(url_for('index')), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

# Decorator para exigir que seja tenant (não admin)
def require_tenant(f):
    """Decorator para exigir que o usuário seja tenant (não admin)"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Se autenticação está desabilitada, permite acesso
        if not AUTH_REQUIRED:
            return f(*args, **kwargs)
        
        # Verifica se usuário está logado
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        
        # Verifica se NÃO é admin (é tenant)
        user_role = session.get('user_role', 'user')
        if user_role == 'admin':
            return redirect(url_for('admin_dashboard'))
        
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

# Importa rotas de organizations
try:
    from web.api.organizations import bp as organizations_bp
    app.register_blueprint(organizations_bp)
    print("[✓] Rotas de organizations registradas")
except Exception as e:
    print(f"[!] Rotas de organizations não disponíveis: {e}")

# Importa rotas administrativas
try:
    from web.api.admin import bp as admin_bp
    app.register_blueprint(admin_bp)
    print("[✓] Rotas administrativas registradas")
except Exception as e:
    print(f"[!] Rotas administrativas não disponíveis: {e}")

# Importa rotas de instâncias
try:
    from web.api.instances import bp as instances_bp
    app.register_blueprint(instances_bp)
    print("[✓] Rotas de instâncias registradas")
except Exception as e:
    print(f"[!] Rotas de instâncias não disponíveis: {e}")

# Importa rotas de agentes
try:
    from web.api.agents import bp as agents_bp
    app.register_blueprint(agents_bp)
    print("[✓] Rotas de agentes registradas")
except Exception as e:
    print(f"[!] Rotas de agentes não disponíveis: {e}")

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
    """Redireciona baseado no role do usuário"""
    if not AUTH_REQUIRED:
        # Modo desenvolvimento - usa dashboard normal
        try:
            return render_template('dashboard_new.html')
        except:
            return render_template('dashboard.html')
    
    # Verifica role do usuário
    user_role = session.get('user_role', 'user')
    
    if user_role == 'admin':
        # Admin vai para área administrativa
        return redirect(url_for('admin_dashboard'))
    else:
        # Tenant vai para área do tenant
        return redirect(url_for('tenant_dashboard'))

@app.route('/admin')
@require_admin
def admin_dashboard():
    """Dashboard administrativo"""
    return render_template('admin/dashboard.html')

@app.route('/tenant/dashboard')
@require_tenant
def tenant_dashboard():
    """Dashboard do tenant"""
    return render_template('tenant/dashboard.html')

@app.route('/simple')
def index_simple():
    """Dashboard simples (sem tenants) - Modo desenvolvimento"""
    config = load_config()
    return render_template('dashboard.html')

# ============================================
# ROTAS - TENANT (Clientes)
# ============================================

@app.route('/tenant/flows')
@require_tenant
def tenant_flows_list():
    """Lista de fluxos do tenant"""
    return render_template('tenant/flows/list.html')

@app.route('/tenant/flows/new')
@require_tenant
def tenant_flows_new():
    """Criar novo fluxo do tenant"""
    return render_template('tenant/flows/new.html')

@app.route('/tenant/notifications')
@require_tenant
def tenant_notifications_list():
    """Lista de notificações do tenant"""
    return render_template('tenant/notifications/list.html')

@app.route('/tenant/leads')
@require_tenant
def tenant_leads_list():
    """Lista de leads do tenant"""
    return render_template('tenant/leads/list.html')

@app.route('/tenant/conversations')
@require_tenant
def tenant_conversations_list():
    """Lista de conversas do tenant"""
    return render_template('tenant/conversations/list.html')

@app.route('/tenant/instances')
@require_tenant
def tenant_instances_list():
    """Lista de instâncias do tenant"""
    tenant_id = request.args.get('tenant_id', type=int)
    return render_template('tenant/instances/list.html', tenant_id=tenant_id)

@app.route('/tenant/qr')
@require_tenant
def tenant_qr_code():
    """Página para escanear QR Code (tenant)"""
    return render_template('tenant/qr.html')

# ============================================
# ROTAS - ADMIN (Compatibilidade - redireciona)
# ============================================

@app.route('/flows')
@require_login
def flows_list():
    """Redireciona para área correta"""
    if not AUTH_REQUIRED:
        return render_template('flows/list.html')
    user_role = session.get('user_role', 'user')
    if user_role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('tenant_flows_list'))

@app.route('/flows/new')
@require_login
def flows_new():
    """Redireciona para área correta"""
    if not AUTH_REQUIRED:
        return render_template('flows/new.html')
    user_role = session.get('user_role', 'user')
    if user_role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('tenant_flows_new'))

@app.route('/notifications')
@require_login
def notifications_list():
    """Redireciona para área correta"""
    if not AUTH_REQUIRED:
        return render_template('notifications/list.html')
    user_role = session.get('user_role', 'user')
    if user_role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('tenant_notifications_list'))

@app.route('/leads')
@require_login
def leads_list():
    """Redireciona para área correta"""
    if not AUTH_REQUIRED:
        return render_template('leads/list.html')
    user_role = session.get('user_role', 'user')
    if user_role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('tenant_leads_list'))

@app.route('/conversations')
@require_login
def conversations_list():
    """Redireciona para área correta"""
    if not AUTH_REQUIRED:
        return render_template('conversations/list.html')
    user_role = session.get('user_role', 'user')
    if user_role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('tenant_conversations_list'))

# ============================================
# ROTAS - TENANTS
# ============================================

@app.route('/admin/organizations')
@require_admin
def admin_organizations_list():
    """Lista de organizações (apenas admin)"""
    return render_template('admin/organizations/list.html')

@app.route('/admin/organizations/new')
@require_admin
def admin_organizations_new():
    """Criar nova organização (apenas admin)"""
    return render_template('admin/organizations/create.html')

@app.route('/admin/organizations/<int:organization_id>')
@require_admin
def admin_organizations_detail(organization_id):
    """Detalhes da organização (apenas admin)"""
    return render_template('admin/organizations/dashboard.html', organization_id=organization_id)

@app.route('/admin/users')
@require_admin
def admin_users_list():
    """Lista de usuários (admin)"""
    return render_template('admin/users/list.html')

@app.route('/admin/instances')
@require_admin
def admin_instances_list():
    """Lista de instâncias (admin)"""
    return render_template('admin/instances/list.html')

@app.route('/admin/settings')
@require_admin
def admin_settings():
    """Configurações do sistema (admin)"""
    return render_template('admin/settings.html')

@app.route('/admin/logs')
@require_admin
def admin_logs():
    """Logs do sistema (admin)"""
    return render_template('admin/logs.html')

@app.route('/admin/analytics')
@require_admin
def admin_analytics():
    """Analytics do sistema (admin)"""
    return render_template('admin/analytics.html')

@app.route('/admin/security')
@require_admin
def admin_security():
    """Segurança do sistema (admin)"""
    return render_template('admin/security.html')

@app.route('/admin/backups')
@require_admin
def admin_backups():
    """Backups do sistema (admin)"""
    return render_template('admin/backups.html')

# Rotas para /organizations (sem /admin) - compatibilidade
@app.route('/organizations')
def organizations_list():
    """Lista de organizações"""
    # Permite acesso sem autenticação em modo desenvolvimento
    if AUTH_REQUIRED:
        if 'user_id' not in session:
            try:
                return redirect(url_for('login_page'))
            except:
                pass
        user_role = session.get('user_role', 'user')
        if user_role == 'admin':
            return redirect(url_for('admin_organizations_list'))
    return render_template('organizations/list.html')

@app.route('/organizations/new')
def organizations_new():
    """Criar nova organização"""
    # Permite acesso sem autenticação em modo desenvolvimento
    if AUTH_REQUIRED:
        # Se autenticação estiver habilitada, verifica login
        if 'user_id' not in session:
            try:
                return redirect(url_for('login_page'))
            except:
                # Se não tiver login_page, permite acesso (modo dev)
                pass
        user_role = session.get('user_role', 'user')
        if user_role == 'admin':
            return redirect(url_for('admin_organizations_new'))
    return render_template('organizations/create.html')

@app.route('/organizations/<int:organization_id>')
def organizations_detail(organization_id):
    """Detalhes da organização"""
    # Permite acesso sem autenticação em modo desenvolvimento
    if AUTH_REQUIRED:
        if 'user_id' not in session:
            try:
                return redirect(url_for('login_page'))
            except:
                pass
    user_role = session.get('user_role', 'user')
    if user_role == 'admin':
        return redirect(url_for('admin_organizations_detail', organization_id=organization_id))
    return render_template('organizations/dashboard.html', organization_id=organization_id)

# ============================================
# ROTAS - INSTÂNCIAS
# ============================================

@app.route('/instances')
@require_login
def instances_list():
    """Lista de instâncias (modo simplificado: redireciona para conexão)"""
    # No modo simplificado, redireciona direto para página de conexão
    from web.utils.instance_helper import get_or_create_user_instance
    from web.utils.auth_helpers import get_current_user_id
    
    user_id = get_current_user_id() or 1
    user_instance = get_or_create_user_instance(user_id)
    
    # Redireciona para página de conexão da instância do usuário
    return redirect(url_for('instances_connect', instance_id=user_instance.get('id')))

@app.route('/instances/new')
def instances_new():
    """Criar nova instância (modo simplificado: redireciona - instância já existe)"""
    # No modo simplificado, a instância é criada automaticamente
    # Redireciona para a instância do usuário
    from web.utils.instance_helper import get_or_create_user_instance
    from web.utils.auth_helpers import get_current_user_id
    
    user_id = get_current_user_id() or 1
    user_instance = get_or_create_user_instance(user_id)
    
    # Redireciona para detalhes da instância (já existe)
    return redirect(url_for('instances_detail', instance_id=user_instance.get('id')))

@app.route('/instances/<int:instance_id>')
@require_login
def instances_detail(instance_id):
    """Detalhes da instância (modo simplificado: redireciona para conexão se não conectado)"""
    # Verifica se é a instância do usuário
    from web.utils.instance_helper import get_or_create_user_instance
    from web.utils.auth_helpers import get_current_user_id
    import requests
    
    user_id = get_current_user_id() or 1
    user_instance = get_or_create_user_instance(user_id)
    
    if user_instance.get('id') != instance_id:
        # Não é a instância do usuário - redireciona para conexão da instância correta
        return redirect(url_for('instances_connect', instance_id=user_instance.get('id')))
    
    # Verifica se está conectado
    try:
        port = user_instance.get('port', 5001)
        status_response = requests.get(f"http://localhost:{port}/status", timeout=1)
        if status_response.status_code == 200:
            status_data = status_response.json()
            actually_connected = status_data.get("actuallyConnected", False)
            ready = status_data.get("ready", False)
            has_qr = status_data.get("hasQr", False)
            
            # Se não está conectado, redireciona para página de conexão
            if not (actually_connected or (ready and not has_qr)):
                return redirect(url_for('instances_connect', instance_id=instance_id))
    except:
        # Se não consegue verificar, redireciona para conexão
        return redirect(url_for('instances_connect', instance_id=instance_id))
    
    return render_template('instances/dashboard.html', instance_id=instance_id)

@app.route('/instances/<int:instance_id>/connect')
@require_login
def instances_connect(instance_id):
    """Conectar WhatsApp da instância"""
    # Verifica se é a instância do usuário (modo simplificado)
    from web.utils.instance_helper import get_or_create_user_instance
    from web.utils.auth_helpers import get_current_user_id
    
    user_id = get_current_user_id() or 1
    user_instance = get_or_create_user_instance(user_id)
    
    if user_instance.get('id') != instance_id:
        # Não é a instância do usuário - redireciona
        return redirect(url_for('instances_connect', instance_id=user_instance.get('id')))
    
    return render_template('instances/connect.html', instance_id=instance_id)

# ============================================
# ROTAS - WHATSAPP
# ============================================

@app.route('/qr')
@require_login
def qr_code():
    """Conecta WhatsApp - modo simplificado: redireciona para instância do usuário"""
    from web.utils.instance_helper import get_or_create_user_instance
    from web.utils.auth_helpers import get_current_user_id
    
    user_id = get_current_user_id() or 1
    user_instance = get_or_create_user_instance(user_id)
    
    # Redireciona para página de conexão da instância do usuário
    return redirect(url_for('instances_connect', instance_id=user_instance.get('id')))

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
        import json
        import os
        
        # Verifica se há instance_id na query string
        instance_id = request.args.get('instance_id', type=int)
        whatsapp_port = whatsapp.port if hasattr(whatsapp, 'port') else 5001
        
        # Se instance_id foi fornecido, busca a porta da instância
        if instance_id:
            orgs_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'organizations.json')
            if os.path.exists(orgs_file):
                try:
                    with open(orgs_file, 'r', encoding='utf-8') as f:
                        organizations = json.load(f)
                        for org in organizations:
                            for inst in org.get('instances', []):
                                if inst.get('id') == instance_id:
                                    whatsapp_port = inst.get('port', whatsapp_port)
                                    break
                except:
                    pass
        
        # Parâmetros opcionais
        only_individuals = request.args.get('only_individuals', 'false').lower() == 'true'
        limit = request.args.get('limit', type=int)
        
        response = requests.get(f"http://localhost:{whatsapp_port}/chats", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Garante formato padronizado
            if isinstance(data, dict) and 'chats' in data:
                chats = data['chats']
            elif isinstance(data, list):
                chats = data
            else:
                chats = []
            
            # Filtra apenas conversas individuais se solicitado
            if only_individuals:
                chats = [c for c in chats if not c.get('isGroup', False)]
            
            # Ordena por timestamp (mais recentes primeiro)
            chats.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
            
            # Limita quantidade se solicitado
            if limit:
                chats = chats[:limit]
            
            return jsonify({
                "success": True,
                "chats": chats,
                "total": len(chats)
            })
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

@app.route('/api/conversations/send', methods=['POST'])
@require_api_auth
def send_message():
    """Envia mensagem via WhatsApp"""
    if not whatsapp:
        return jsonify({"success": False, "error": "WhatsApp não inicializado"}), 500
    
    try:
        data = request.get_json()
        phone = data.get('phone')
        message = data.get('message')
        
        if not phone or not message:
            return jsonify({"success": False, "error": "Telefone e mensagem são obrigatórios"}), 400
        
        # Envia via WhatsApp
        success = whatsapp.send_message(phone, message)
        
        if success:
            return jsonify({"success": True, "message": "Mensagem enviada com sucesso"})
        else:
            return jsonify({"success": False, "error": "Erro ao enviar mensagem"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/flows/check', methods=['GET'])
@require_api_auth
def check_active_flow():
    """Verifica se há fluxo ativo para um número"""
    try:
        phone = request.args.get('phone')
        if not phone:
            return jsonify({"success": False, "error": "Telefone é obrigatório"}), 400
        
        # Remove formatação do número
        phone = phone.replace('@c.us', '').replace('@s.whatsapp.net', '').replace('+', '').replace(' ', '')
        
        # Verifica fluxos ativos
        from src.flows.flow_engine import flow_engine
        
        # Procura fluxo que pode ser ativado para este número
        active_flow = None
        for flow_id, flow_data in flow_engine.active_flows.items():
            trigger = flow_data.get('trigger', {})
            trigger_type = trigger.get('type', 'always')
            
            # Se for 'always', está ativo
            if trigger_type == 'always':
                active_flow = {
                    'id': flow_id,
                    'name': flow_data.get('name', 'Fluxo sem nome')
                }
                break
        
        if active_flow:
            return jsonify({"success": True, "flow": active_flow})
        else:
            return jsonify({"success": True, "flow": None})
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/whatsapp-status')
def whatsapp_status():
    """Status da conexão WhatsApp (modo simplificado: usa instância do usuário)"""
    try:
        from web.utils.instance_helper import get_or_create_user_instance
        from web.utils.auth_helpers import get_current_user_id
        import requests
        
        # Obtém instância do usuário
        user_id = get_current_user_id() or 1
        instance = get_or_create_user_instance(user_id)
        whatsapp_port = instance.get('port', 5001)
        
        # Verifica status do servidor Node.js da instância do usuário
        try:
            status_response = requests.get(f"http://localhost:{whatsapp_port}/status", timeout=1)
            if status_response.status_code == 200:
                status_data = status_response.json()
                has_qr = status_data.get("hasQr", False)
                actually_connected = status_data.get("actuallyConnected", False)
                ready = status_data.get("ready", False)
                
                # Só considera conectado se realmente estiver conectado
                connected = actually_connected or (ready and not has_qr)
                
                if connected:
                    return jsonify({
                        "connected": True, 
                        "message": "WhatsApp conectado",
                        "hasQr": False,
                        "port": whatsapp_port
                    })
                elif has_qr:
                    return jsonify({
                        "connected": False, 
                        "message": "QR Code disponível. Escaneie para conectar.",
                        "hasQr": True,
                        "port": whatsapp_port
                    })
                else:
                    return jsonify({
                        "connected": False, 
                        "message": "Aguardando conexão. Clique em 'Conectar WhatsApp' para gerar QR Code.",
                        "hasQr": False,
                        "port": whatsapp_port
                    })
        except requests.exceptions.ConnectionError:
            return jsonify({
                "connected": False, 
                "error": f"Servidor WhatsApp não está rodando na porta {whatsapp_port}",
                "hasQr": False,
                "port": whatsapp_port
            })
        except requests.exceptions.RequestException as e:
            return jsonify({
                "connected": False, 
                "error": f"Erro ao conectar com servidor: {str(e)}",
                "hasQr": False,
                "port": whatsapp_port
            })
            
    except Exception as e:
        return jsonify({"connected": False, "error": str(e), "hasQr": False})

@app.route('/api/whatsapp-disconnect', methods=['POST'])
@require_api_auth
def whatsapp_disconnect():
    """Desconecta o WhatsApp"""
    if not whatsapp:
        return jsonify({"success": False, "error": "WhatsApp não inicializado"}), 400
    
    try:
        import requests
        whatsapp_port = whatsapp.port if hasattr(whatsapp, 'port') else 5001
        
        # Chama endpoint de desconexão do servidor Node.js
        try:
            response = requests.post(f"http://localhost:{whatsapp_port}/disconnect", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return jsonify({
                    "success": True,
                    "message": data.get("message", "WhatsApp desconectado com sucesso")
                })
            else:
                return jsonify({"success": False, "error": "Erro ao desconectar"}), 500
        except requests.exceptions.RequestException as e:
            return jsonify({"success": False, "error": f"Erro ao conectar com servidor: {str(e)}"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

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
@rate_limit_whatsapp  # Rate limiting para webhook (envio de mensagens)
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
        
        # Tenta identificar instance_id (pode vir no request ou buscar pelo número)
        instance_id = data.get('instance_id')
        tenant_id = data.get('tenant_id')
        
        # Se não fornecido, tenta buscar pela conversa
        if not instance_id:
            try:
                from src.database.db import SessionLocal
                from src.models.conversation import Conversation
                db = SessionLocal()
                try:
                    # Busca conversa mais recente com este telefone
                    conversation = db.query(Conversation).filter(
                        Conversation.phone == phone
                    ).order_by(Conversation.last_message_at.desc()).first()
                    
                    if conversation:
                        instance_id = conversation.instance_id
                        if not tenant_id:
                            tenant_id = conversation.tenant_id
                finally:
                    db.close()
            except Exception as e:
                print(f"[!] Erro ao buscar instance_id: {e}")
        
        print(f"[📨] Mensagem recebida de {phone}: {message} (instance_id={instance_id}, tenant_id={tenant_id})")
        
        # Tenta processar com fluxos primeiro
        try:
            from src.whatsapp.message_handler import message_handler
            
            # Processa mensagem com fluxos
            flow_result = message_handler.process_message(
                phone=phone,
                message=message,
                tenant_id=tenant_id,
                instance_id=instance_id,
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
            response = ai.get_response(phone, message, tenant_id=tenant_id, instance_id=instance_id)
            print(f"[🤖] Resposta da IA: {response}")
            
            # Envia resposta via WhatsApp (usando fila)
            if whatsapp and response:
                from web.utils.message_sender import send_message_via_queue
                from web.utils.auth_helpers import get_current_tenant_id
                
                tenant_id = get_current_tenant_id()
                result = send_message_via_queue(
                    phone=phone,
                    message=response,
                    tenant_id=tenant_id,
                    priority=1,  # Prioridade média para respostas automáticas
                    use_queue=True
                )
                
                if result.get('success'):
                    if result.get('via_queue'):
                        print(f"[✓] Resposta adicionada à fila para {phone}")
                    else:
                        print(f"[✓] Resposta enviada diretamente para {phone}")
                else:
                    print(f"[!] Erro ao enviar resposta para {phone}: {result.get('error')}")
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
# INICIALIZAÇÃO DO RATE LIMITER
# ============================================

# Inicializa rate limiter
redis_url = REDIS_URL if USE_REDIS else None
init_rate_limiter(app, redis_url=redis_url)

# ============================================
# INICIALIZAÇÃO DA FILA DE MENSAGENS
# ============================================

# Inicializa fila de mensagens
message_queue_instance = init_message_queue(redis_url=redis_url, use_redis=USE_REDIS)

# Inicializa worker de mensagens (em thread separada)
def start_message_worker():
    """Inicia worker de mensagens em thread separada"""
    if whatsapp and message_queue_instance:
        try:
            worker = init_message_worker(message_queue_instance, whatsapp, interval=1.0)
            worker_thread = threading.Thread(target=worker.start, daemon=True)
            worker_thread.start()
            print("[✓] Worker de mensagens iniciado em background")
        except Exception as e:
            print(f"[!] Erro ao iniciar worker de mensagens: {e}")

# ============================================
# INICIALIZAÇÃO DO SERVIDOR WHATSAPP
# ============================================

# Exporta app para Vercel
application = app

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
    
    # Inicia worker de mensagens (aguarda um pouco para garantir que tudo está pronto)
    import time
    time.sleep(2)
    try:
        start_message_worker()
    except Exception as e:
        print(f"[!] Erro ao iniciar worker de mensagens: {e}")
    
    # Inicia Flask
    port = int(os.getenv('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=True)

