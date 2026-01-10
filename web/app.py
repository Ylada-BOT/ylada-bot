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
import time
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path

# Carrega variáveis de ambiente do .env
try:
    from dotenv import load_dotenv
    from pathlib import Path
    env_path = Path(__file__).resolve().parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"[✓] Variáveis de ambiente carregadas de {env_path}")
except ImportError:
    print("[!] python-dotenv não instalado. Instale com: pip install python-dotenv")
except Exception as e:
    print(f"[!] Erro ao carregar .env: {e}")

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
CORS(app, supports_credentials=True)  # Permite envio de cookies

# ============================================
# CONFIGURAÇÃO DE LOGGING CENTRALIZADO
# ============================================
BASE_DIR = Path(__file__).resolve().parent.parent
log_dir = BASE_DIR / 'logs'
log_dir.mkdir(exist_ok=True)

# Handler para arquivo (rotação automática)
file_handler = RotatingFileHandler(
    log_dir / 'app.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

# Handler para console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(message)s'
))

# Configurar logger do app
app.logger.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)

# Desabilitar logs verbosos do Werkzeug
logging.getLogger('werkzeug').setLevel(logging.WARNING)

# Logger para este módulo
logger = app.logger
logger.info("="*60)
logger.info("🚀 Iniciando BOT by YLADA")
logger.info("="*60)

# ============================================
# VALIDAÇÃO DE CONFIGURAÇÕES
# ============================================
def validate_configuration():
    """Valida configurações críticas na inicialização"""
    from config.settings import WHATSAPP_SERVER_URL, IS_PRODUCTION, DATABASE_URL
    
    errors = []
    warnings = []
    
    if IS_PRODUCTION:
        # Validar WHATSAPP_SERVER_URL em produção
        if not WHATSAPP_SERVER_URL or 'localhost' in WHATSAPP_SERVER_URL:
            errors.append(
                "❌ WHATSAPP_SERVER_URL não configurado em produção!\n"
                "   Configure no Railway: WHATSAPP_SERVER_URL=http://whatsapp-server-2:5001"
            )
        
        # Validar DATABASE_URL
        if not DATABASE_URL or 'localhost' in DATABASE_URL:
            warnings.append(
                "⚠️  DATABASE_URL parece estar em modo desenvolvimento.\n"
                "   Verifique se está usando a connection string do Supabase."
            )
    else:
        # Em desenvolvimento, apenas avisa
        if not WHATSAPP_SERVER_URL:
            warnings.append(
                "⚠️  WHATSAPP_SERVER_URL não configurado.\n"
                "   Usando padrão: http://localhost:5001"
            )
    
    if errors:
        logger.error("\n" + "="*60)
        logger.error("⚠️  ERROS DE CONFIGURAÇÃO DETECTADOS:")
        logger.error("="*60)
        for error in errors:
            logger.error(error)
        logger.error("="*60 + "\n")
        # Em produção, não trava o servidor, apenas avisa
        if not IS_PRODUCTION:
            raise ValueError("Configurações inválidas. Corrija antes de continuar.")
    
    if warnings:
        logger.warning("\n" + "="*60)
        logger.warning("⚠️  AVISOS DE CONFIGURAÇÃO:")
        logger.warning("="*60)
        for warning in warnings:
            logger.warning(warning)
        logger.warning("="*60 + "\n")
    
    return len(errors) == 0

# Executar validação após criar o app
try:
    validate_configuration()
    logger.info("✅ Configurações validadas com sucesso")
except Exception as e:
    logger.error(f"❌ Erro na validação de configurações: {e}")

# ============================================
# HANDLERS DE ERRO GLOBAL
# ============================================
from werkzeug.exceptions import HTTPException
from web.utils.error_messages import format_error_response

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
        logger.error(f"Erro não tratado em {request.path}: {e}", exc_info=True)
        return format_error_response(e, context=f"em {request.path}", status_code=500)
    
    # Para rotas não-API, deixa o Flask tratar normalmente
    raise e

# Configuração de sessão
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuração de autenticação
# Defina AUTH_REQUIRED=false para desabilitar autenticação (apenas desenvolvimento)
# Por padrão, ATIVADO para separar contas e System Prompts
AUTH_REQUIRED = os.getenv('AUTH_REQUIRED', 'true').lower() == 'true'

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
    print("[✓] Rotas de autenticação registradas")
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

# Importa rotas de diagnóstico
try:
    from web.api.diagnostic import diagnostic_bp
    app.register_blueprint(diagnostic_bp)
    print("[✓] Rotas de diagnóstico registradas")
except Exception as e:
    print(f"[!] Rotas de diagnóstico não disponíveis: {e}")

# Importa rotas de configuração do WhatsApp
try:
    from web.api.whatsapp_config import bp as whatsapp_config_bp
    app.register_blueprint(whatsapp_config_bp)
    print("[✓] Rotas de configuração do WhatsApp registradas")
except Exception as e:
    print(f"[!] Rotas de configuração do WhatsApp não disponíveis: {e}")

# API de Campanhas (Envio em Massa)
try:
    from web.api.campaigns import bp as campaigns_bp
    app.register_blueprint(campaigns_bp)
    logger.info("✅ API de Campanhas (envio em massa) registrada")
except Exception as e:
    logger.warning(f"⚠️ API de Campanhas não disponível: {e}")

# API de Conversas (Funcionalidades Avançadas)
try:
    from web.api.conversations import bp as conversations_api_bp
    app.register_blueprint(conversations_api_bp)
    logger.info("✅ API de Conversas (funcionalidades avançadas) registrada")
except Exception as e:
    logger.warning(f"⚠️ API de Conversas não disponível: {e}")

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

# Carrega configuração inicial da IA do .env
try:
    initial_config = {
        'provider': os.getenv('AI_PROVIDER', 'openai'),
        'api_key': os.getenv('AI_API_KEY', ''),
        'model': os.getenv('AI_MODEL', 'gpt-4o-mini'),
        'system_prompt': os.getenv('AI_SYSTEM_PROMPT', 'Você é um assistente útil e amigável.')
    }
    if initial_config['api_key']:
        ai.set_config(
            provider=initial_config['provider'],
            api_key=initial_config['api_key'],
            model=initial_config['model'],
            system_prompt=initial_config['system_prompt']
        )
        print(f"[✓] IA configurada com API Key do .env (Provider: {initial_config['provider']}, Model: {initial_config['model']})")
    else:
        print("[!] AI_API_KEY não encontrada no .env. Configure no dashboard.")
except Exception as e:
    print(f"[!] Erro ao configurar IA inicialmente: {e}")
print("[✓] IA Handler inicializado")

# Configuração (salva por usuário)
def get_config_file(user_id=None):
    """Retorna caminho do arquivo de config do usuário"""
    if user_id:
        return os.path.join(os.path.dirname(__file__), '..', 'data', f'ai_config_user_{user_id}.json')
    return os.path.join(os.path.dirname(__file__), '..', 'data', 'ai_config.json')

def load_config(user_id=None):
    """Carrega configuração da IA (do arquivo do usuário ou .env)"""
    from web.utils.auth_helpers import get_current_user_id
    from flask import has_request_context
    
    # Se não passou user_id, tenta pegar do usuário logado (só se houver requisição)
    if not user_id and has_request_context():
        try:
            user_id = get_current_user_id()
        except:
            user_id = None
    
    CONFIG_FILE = get_config_file(user_id)
    
    config = {
        'provider': os.getenv('AI_PROVIDER', 'openai'),
        'api_key': os.getenv('AI_API_KEY', ''),  # API key global do .env
        'model': os.getenv('AI_MODEL', 'gpt-4o-mini'),
        'system_prompt': os.getenv('AI_SYSTEM_PROMPT', 'Você é um assistente útil e amigável.')
    }
    
    # Se existe arquivo de config do usuário, usa ele (tem prioridade sobre .env)
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                # Mescla: arquivo tem prioridade, mas .env preenche valores vazios
                for key in config:
                    if file_config.get(key):
                        config[key] = file_config[key]
                # API key: se não tem no arquivo, usa do .env
                if not config.get('api_key'):
                    config['api_key'] = os.getenv('AI_API_KEY', '')
        except:
            pass
    
    # Aplica configuração na IA
    try:
        ai.set_config(
            provider=config['provider'],
            api_key=config['api_key'],
            model=config['model'],
            system_prompt=config['system_prompt']
        )
    except Exception as e:
        print(f"[!] Erro ao configurar IA: {e}")
    
    return config

def save_config(config, user_id=None):
    """Salva configuração da IA (por usuário)"""
    from web.utils.auth_helpers import get_current_user_id
    
    # Se não passou user_id, tenta pegar do usuário logado
    if not user_id:
        user_id = get_current_user_id()
    
    CONFIG_FILE = get_config_file(user_id)
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# Carrega configuração padrão ao iniciar (para desenvolvimento)
# Em produção com login, cada usuário terá sua própria config ao fazer login
if not AUTH_REQUIRED:
    try:
        # Tenta carregar config padrão (sem user_id)
        from web.utils.auth_helpers import get_current_user_id
        load_config(None)  # Passa None explicitamente
        print("[✓] Configuração padrão da IA carregada")
    except:
        print("[!] Configuração da IA será carregada por usuário ao fazer login")
else:
    print("[✓] Sistema com login ativado - configuração será carregada por usuário")

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

@app.route('/favicon.ico')
def favicon():
    """Retorna favicon (evita erro 404)"""
    # Retorna 204 No Content (sem erro, apenas sem conteúdo)
    # Isso evita o erro 404 no console
    from flask import Response
    return Response(status=204)

@app.route('/static/manifest.json')
def manifest():
    """Retorna manifest.json para PWA"""
    from flask import send_from_directory
    return send_from_directory(
        os.path.join(os.path.dirname(__file__), 'static'),
        'manifest.json',
        mimetype='application/manifest+json'
    )

@app.route('/static/uploads/<path:filename>')
def serve_upload(filename):
    """Serve arquivos de upload (fotos de perfil, etc)"""
    from flask import send_from_directory
    from pathlib import Path
    from config.settings import UPLOAD_FOLDER
    
    # Remove 'profiles/' do caminho se estiver presente
    if filename.startswith('profiles/'):
        filename = filename.replace('profiles/', '')
        upload_dir = Path(UPLOAD_FOLDER) / 'profiles'
    else:
        upload_dir = Path(UPLOAD_FOLDER)
    
    return send_from_directory(str(upload_dir), filename)

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

@app.route('/profile')
@require_login
def profile_page():
    """Página de perfil do usuário"""
    return render_template('profile.html')

@app.route('/whatsapp-logo-setup')
def whatsapp_logo_setup():
    """Página para configurar logo no WhatsApp"""
    return render_template('whatsapp_logo_setup.html')

# ============================================
# ROTAS - DASHBOARD
# ============================================

@app.route('/')
def index():
    """Página inicial (landing page) ou Dashboard se logado"""
    # Se autenticação está desabilitada, mostra dashboard direto
    if not AUTH_REQUIRED:
        return render_template('dashboard_new.html')
    
    # Se usuário não está logado, mostra landing page
    if 'user_id' not in session:
        return render_template('landing.html')
    
    # Se usuário está logado, redireciona para dashboard
    user_role = session.get('user_role', 'user')
    if user_role == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    # Carrega config do usuário logado
    user_id = session.get('user_id')
    if user_id:
        try:
            load_config(user_id)
        except:
            pass
    
    return render_template('dashboard_new.html')

@app.route('/dashboard')
@require_login
def dashboard():
    """Dashboard principal (rota alternativa)"""
    # Se autenticação está desabilitada, mostra dashboard direto
    if not AUTH_REQUIRED:
            return render_template('dashboard_new.html')
    
    # Se usuário é admin, redireciona para área administrativa
    user_role = session.get('user_role', 'user')
    if user_role == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    # Se autenticação está habilitada, carrega config do usuário logado
    user_id = session.get('user_id')
    if user_id:
        try:
            load_config(user_id)
        except:
            pass
    
    return render_template('dashboard_new.html')

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
    user_id = session.get('user_id') if AUTH_REQUIRED else None
    config = load_config(user_id)
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
    """Lista de conversas do tenant - Redireciona para modelo simplificado"""
    # No modelo simplificado, usa o template direto
    return render_template('conversations/list.html')

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
    """Lista de conversas - Modelo Simplificado"""
    # No modelo simplificado, sempre usa o template direto
    return render_template('conversations/list.html')

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
    
    # Redireciona para página de conexão simples
    return redirect(url_for('qr_code'))

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
        # Não é a instância do usuário - redireciona para conexão simples
        return redirect(url_for('qr_code'))
    
    # Verifica se está conectado
    try:
        from web.utils.instance_helper import get_whatsapp_server_url
        port = user_instance.get('port', 5001)
        server_url = get_whatsapp_server_url(port)
        # IMPORTANTE: Passa user_id para verificar status do usuário correto
        status_response = requests.get(f"{server_url}/status?user_id={user_id}", timeout=1)
        if status_response.status_code == 200:
            status_data = status_response.json()
            actually_connected = status_data.get("actuallyConnected", False)
            ready = status_data.get("ready", False)
            has_qr = status_data.get("hasQr", False)
            
            # Se não está conectado, redireciona para página de conexão
            if not (actually_connected or (ready and not has_qr)):
                return redirect(url_for('qr_code'))
    except:
        # Se não consegue verificar, redireciona para conexão
        return redirect(url_for('qr_code'))
    
    return render_template('instances/dashboard.html', instance_id=instance_id)

@app.route('/instances/<int:instance_id>/connect')
@require_login
def instances_connect(instance_id):
    """Conectar WhatsApp da instância - redireciona para /connect (modo simplificado)"""
    # No modelo simplificado, redireciona para rota simples
    return redirect(url_for('qr_code'))

# ============================================
# ROTAS - WHATSAPP
# ============================================

@app.route('/qr')
@app.route('/connect')
@require_login
def qr_code():
    """Conecta WhatsApp - modo simplificado: página direta sem instance_id"""
    # No modelo simplificado, não precisa de instance_id
    # Cada usuário tem apenas 1 instância
    return render_template('instances/connect.html')

@app.route('/api/qr')
def get_qr():
    """Obtém QR Code do WhatsApp - Modelo Simplificado"""
    try:
        from web.utils.instance_helper import get_or_create_user_instance, ensure_whatsapp_server_running, get_whatsapp_server_url
        from web.utils.auth_helpers import get_current_user_id as get_user_id
        import requests
        
        # Obtém instância do usuário
        try:
            user_id = get_user_id() or 1
        except:
            user_id = 1  # Fallback para desenvolvimento
        
        # Permite especificar instance_id via query string
        instance_id = request.args.get('instance_id', type=int)
        instance = get_or_create_user_instance(user_id, instance_id)
        if not instance:
            return jsonify({
                "error": "Instância não encontrada",
                "status": "error"
            }), 404
        
        port = instance.get('port', 5001)
        
        # IMPORTANTE: Usa user_id_instance_id para identificar instância única
        from web.utils.instance_helper import get_instance_user_id
        unique_user_id = get_instance_user_id(user_id, instance.get('id', user_id))
        
        print(f"[*] Usuário {user_id}, Instância {instance.get('id')} solicitando QR code na porta {port}")
        
        # Obtém URL do servidor WhatsApp
        from config.settings import IS_PRODUCTION
        server_url = get_whatsapp_server_url(port)
        
        # Não bloqueia aqui - deixa o retry do http_client tentar conectar
        # Se o servidor não estiver disponível, o retry vai lidar com isso
        logger.info(f"Buscando QR Code do servidor WhatsApp em {server_url} para user_id={unique_user_id}")
        
        # Busca QR Code do servidor Node.js
        # Passa unique_user_id para separar sessões por instância
        base_url = server_url.rstrip('/')
        qr_url = f"{base_url}/qr?user_id={unique_user_id}"
        
        # Usa http_client com retry para comunicação robusta
        from web.utils.http_client import get_with_retry
        
        try:
            # Tenta buscar QR Code com retry (até 3 tentativas) e timeout maior
            # Timeout aumentado para 30s porque servidor pode estar lento gerando QR Code
            response = get_with_retry(qr_url, timeout=30, max_retries=3)
            if response.status_code == 200:
                data = response.json()
                
                # Se já está conectado
                if data.get('ready'):
                    return jsonify({"status": "connected"})
                
                # Se tem QR code, retorna
                qr_data = data.get('qr')
                if qr_data:
                    return jsonify({
                        "qr": qr_data, 
                        "status": "waiting",
                        "success": True
                    })
                
                # Se não tem QR ainda, verifica se precisa reiniciar o cliente
                # Se o cliente está inicializado mas não tem QR e não está pronto, pode precisar reiniciar
                if not data.get('ready') and not qr_data:
                    message = data.get('message', 'Aguardando geração do QR Code...')
                    return jsonify({
                        "status": "generating",
                        "message": message,
                        "success": True,
                        "hint": "O servidor está aguardando o WhatsApp gerar o QR code. Isso pode levar 10-30 segundos. Se demorar mais, recarregue a página."
                    })
                
                # Se não tem QR ainda, verifica se o servidor retornou uma mensagem
                server_message = data.get('message', 'Aguardando geração do QR Code...')
                return jsonify({
                    "status": "generating",
                    "message": server_message,
                    "success": True,
                    "hint": "O servidor está aguardando o WhatsApp gerar o QR code. Isso pode levar 10-30 segundos. Se demorar mais, recarregue a página."
                })
                
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as conn_error:
            error_msg = f"Servidor WhatsApp não está acessível na porta {port}."
            logger.error(f"[!] {error_msg}: {conn_error}")
            logger.error(f"[!] Tentando acessar: {qr_url}")
            
            # Em produção, não tenta iniciar automaticamente
            from config.settings import IS_PRODUCTION
            if IS_PRODUCTION:
                return jsonify({
                    "error": "Servidor WhatsApp não está acessível. O serviço Node.js precisa estar rodando.",
                    "status": "error",
                    "message": "Erro 503: Servidor WhatsApp não está disponível",
                    "port": port,
                    "hint": f"Em produção, o servidor WhatsApp precisa estar rodando como um serviço separado. Verifique se o serviço está ativo no Railway.",
                    "server_url": server_url,
                    "solution": "Tente recarregar a página (F5) em alguns segundos ou verifique se o serviço WhatsApp está ativo no Railway."
                }), 503
            
            # Em desenvolvimento, tenta iniciar automaticamente
            print(f"[*] Tentando iniciar servidor automaticamente...")
            server_started = ensure_whatsapp_server_running(port)
            if server_started:
                time.sleep(3)
                # Tenta novamente após iniciar
            try:
                response = get_with_retry(qr_url, timeout=15, max_retries=2)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('ready'):
                        return jsonify({"status": "connected"})
                    qr_data = data.get('qr')
                    if qr_data:
                        return jsonify({
                            "qr": qr_data, 
                            "status": "waiting",
                            "success": True
                        })
            except Exception as retry_error:
                    print(f"[!] Erro ao tentar novamente: {retry_error}")
            
            return jsonify({
                "error": error_msg + " Tente recarregar a página em alguns segundos.",
                "status": "error",
                "port": port,
                "hint": f"Verifique se o servidor Node.js está rodando. Execute: node whatsapp_server.js",
                "server_url": server_url
            }), 503
        except requests.exceptions.Timeout:
            return jsonify({
                "error": f"Timeout ao conectar com servidor WhatsApp na porta {port}.",
                "status": "error"
            }), 503
        except Exception as e:
            return jsonify({
                "error": f"Erro ao conectar com servidor WhatsApp: {str(e)}",
                "status": "error"
            }), 503
    except Exception as e:
        import traceback
        return jsonify({
            "error": str(e),
            "status": "error",
            "traceback": traceback.format_exc() if app.debug else None
        }), 500

@app.route('/api/conversations')
@require_api_auth
def get_conversations():
    """Obtém lista de conversas do WhatsApp - Modelo Simplificado"""
    try:
        from web.utils.instance_helper import get_or_create_user_instance, get_whatsapp_server_url
        from web.utils.auth_helpers import get_current_user_id
        import requests
        
        # Obtém instância do usuário atual
        user_id = get_current_user_id() or 1
        # Permite instance_id via query string ou JSON body
        instance_id = request.args.get('instance_id', type=int) or (request.get_json() or {}).get('instance_id')
        
        instance = get_or_create_user_instance(user_id, instance_id)
        if not instance:
            return jsonify({
                "success": False,
                "error": "Instância não encontrada"
            }), 404
        
        whatsapp_port = instance.get('port', 5001)
        server_url = get_whatsapp_server_url(whatsapp_port)
        
        # IMPORTANTE: Usa user_id_instance_id para identificar instância única
        from web.utils.instance_helper import get_instance_user_id
        unique_user_id = get_instance_user_id(user_id, instance.get('id', user_id))
        
        # PRIMEIRO: Verifica se o servidor está acessível (health check)
        from web.utils.http_client import get_with_retry
        from web.utils.error_messages import format_error_response
        import requests  # Mantido para compatibilidade
        
        try:
            health_response = get_with_retry(f"{server_url}/health", timeout=10, max_retries=2)
            if health_response.status_code != 200:
                return format_error_response(
                    Exception(f"Servidor retornou status {health_response.status_code}"),
                    context="ao verificar saúde do servidor WhatsApp",
                    operation="verificar servidor WhatsApp",
                    status_code=503
                )
        except Exception as e:
            logger.error(f"Erro ao verificar servidor WhatsApp: {e}")
            return format_error_response(
                e,
                context=f"ao conectar ao servidor WhatsApp em {server_url}",
                operation="verificar servidor WhatsApp",
                status_code=503
            )
        
        # SEGUNDO: Verifica se o WhatsApp está conectado
        try:
            status_response = get_with_retry(f"{server_url}/status?user_id={unique_user_id}", timeout=10, max_retries=2)
            if status_response.status_code == 200:
                status_data = status_response.json()
                actually_connected = status_data.get("actuallyConnected", False)
                ready = status_data.get("ready", False)
                has_qr = status_data.get("hasQr", False)
                
                # Verifica se realmente está conectado
                is_connected = False
                if actually_connected:
                    is_connected = True
                elif ready and not has_qr:
                    is_connected = True
                
                if not is_connected:
                    return jsonify({
                        "success": False,
                        "error": "WhatsApp não está conectado",
                        "details": "Conecte o WhatsApp primeiro escaneando o QR Code na página 'Conectar WhatsApp'.",
                        "has_qr": has_qr,
                        "needs_qr": has_qr
                    }), 400
        except requests.exceptions.RequestException:
            # Se não conseguir verificar status, continua tentando buscar conversas
            # (pode ser que o endpoint /status não exista em versões antigas)
            pass
        
        # TERCEIRO: Busca as conversas
        # Parâmetros opcionais
        only_individuals = request.args.get('only_individuals', 'false').lower() == 'true'
        limit = request.args.get('limit', type=int)
        
        # IMPORTANTE: Passa unique_user_id para separar conversas por instância
        response = get_with_retry(f"{server_url}/chats", timeout=15, max_retries=2, params={"user_id": unique_user_id})
        
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
        elif response.status_code == 400:
            # Servidor retornou 400 - provavelmente cliente não conectado
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
            error_msg = error_data.get('error', 'Cliente WhatsApp não conectado')
            return jsonify({
                "success": False,
                "error": error_msg,
                "details": "Escaneie o QR Code na página 'Conectar WhatsApp' para conectar sua conta."
            }), 400
        else:
            return jsonify({
                "success": False, 
                "error": f"Erro ao buscar conversas (status {response.status_code})",
                "details": "O servidor WhatsApp retornou um erro. Verifique os logs do servidor."
            }), 500
            
    except Exception as e:
        logger.error(f"Erro em get_conversations: {e}", exc_info=True)
        return format_error_response(
            e,
            context="ao carregar conversas",
            operation="carregar conversas",
            status_code=503 if isinstance(e, (requests.exceptions.ConnectionError, requests.exceptions.Timeout)) else 500
        )

@app.route('/api/conversations/<chat_id>/messages')
@require_api_auth
def get_conversation_messages(chat_id):
    """Obtém mensagens de uma conversa específica - Modelo Simplificado"""
    try:
        from web.utils.instance_helper import get_or_create_user_instance, get_whatsapp_server_url
        from web.utils.auth_helpers import get_current_user_id
        import requests
        
        # Obtém instância do usuário atual
        user_id = get_current_user_id() or 1
        instance_id = request.args.get('instance_id', type=int)
        
        instance = get_or_create_user_instance(user_id, instance_id)
        if not instance:
            return jsonify({"success": False, "error": "Instância não encontrada"}), 404
        
        whatsapp_port = instance.get('port', 5001)
        server_url = get_whatsapp_server_url(whatsapp_port)
        
        # IMPORTANTE: Usa user_id_instance_id para identificar instância única
        from web.utils.instance_helper import get_instance_user_id
        unique_user_id = get_instance_user_id(user_id, instance.get('id', user_id))
        
        limit = request.args.get('limit', 50, type=int)
        # IMPORTANTE: Passa unique_user_id para separar mensagens por instância
        response = get_with_retry(
            f"{server_url}/chats/{chat_id}/messages",
            timeout=15,
            max_retries=2,
            params={"limit": limit, "user_id": unique_user_id}
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return format_error_response(
                Exception(f"Servidor retornou status {response.status_code}"),
                context="ao buscar mensagens",
                operation="buscar mensagens",
                status_code=500
            )
            
    except Exception as e:
        logger.error(f"Erro em get_conversation_messages: {e}", exc_info=True)
        return format_error_response(
            e,
            context="ao buscar mensagens",
            operation="buscar mensagens",
            status_code=503 if isinstance(e, (requests.exceptions.ConnectionError, requests.exceptions.Timeout)) else 500
        )

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
        from web.utils.instance_helper import get_or_create_user_instance, get_whatsapp_server_url
        from web.utils.auth_helpers import get_current_user_id
        import requests
        
        # Obtém instância do usuário
        user_id = get_current_user_id() or 1
        instance_id = request.args.get('instance_id', type=int)
        
        instance = get_or_create_user_instance(user_id, instance_id)
        if not instance:
            return jsonify({
                "connected": False,
                "error": "Instância não encontrada",
                "hasQr": False
            }), 404
        
        whatsapp_port = instance.get('port', 5001)
        server_url = get_whatsapp_server_url(whatsapp_port)
        
        # IMPORTANTE: Usa user_id_instance_id para identificar instância única
        from web.utils.instance_helper import get_instance_user_id
        unique_user_id = get_instance_user_id(user_id, instance.get('id', user_id))
        
        # Verifica status do servidor Node.js da instância do usuário
        try:
            status_response = requests.get(f"{server_url}/status?user_id={unique_user_id}", timeout=3)
            if status_response.status_code == 200:
                status_data = status_response.json()
                has_qr = status_data.get("hasQr", False)
                actually_connected = status_data.get("actuallyConnected", False)
                ready = status_data.get("ready", False)
                
                # Só considera conectado se realmente estiver conectado
                # Verifica múltiplos indicadores para garantir conexão real
                is_connected = False
                
                # PRIORIDADE 1: actuallyConnected é o mais confiável
                if actually_connected:
                    is_connected = True
                # PRIORIDADE 2: ready + clientInfo com wid válido
                elif ready and status_data.get('clientInfo'):
                    client_info = status_data.get('clientInfo', {})
                    wid = client_info.get('wid')
                    # Wid válido não deve ser None e não deve ser temporário
                    if wid and '@temp' not in str(wid):
                        is_connected = True
                # PRIORIDADE 3: ready sem QR (pode ser conexão, mas menos confiável)
                elif ready and not has_qr:
                    # Só confia se não tiver QR e estiver marcado como ready
                    is_connected = True
                # PRIORIDADE 4: Se está autenticado mas ainda não ready (processo de conexão)
                is_authenticated = status_data.get('isAuthenticated', False)
                if is_authenticated and not has_qr:
                    # Se está autenticado e não tem QR, está conectando ou conectado
                    # WhatsApp Web.js pode estar no processo de inicialização
                    is_connected = True
                    logger.info(f"Detectado estado 'authenticated' sem QR - considerando conectado para user_id={unique_user_id}")
                # PRIORIDADE 5: Se não tem QR e não está ready, mas tem clientInfo válido
                elif not has_qr and status_data.get('clientInfo'):
                    client_info = status_data.get('clientInfo', {})
                    wid = client_info.get('wid')
                    # Se tem wid válido, mesmo que não esteja ready ainda, considera conectando
                    if wid and '@temp' not in str(wid):
                        # Marca como conectado mas pode estar ainda inicializando
                        is_connected = True
                
                connected = is_connected
                
                # Extrai número do telefone se estiver conectado
                # Primeiro tenta usar phone_number do servidor Node.js (já formatado)
                phone_number = status_data.get('phone_number')
                if not phone_number and connected:
                    # Fallback: tenta obter o número do telefone do objeto actually_connected ou ready
                    if isinstance(actually_connected, dict) and 'user' in actually_connected:
                        phone_number = actually_connected.get('user')
                    elif isinstance(ready, dict) and 'user' in ready:
                        phone_number = ready.get('user')
                    elif status_data.get('clientInfo') and status_data['clientInfo'].get('wid'):
                        phone_number = status_data['clientInfo']['wid']
                    
                    # Formata o número para exibição (adiciona formatação brasileira se necessário)
                    if phone_number:
                        # Remove @c.us se houver
                        phone_number = phone_number.replace('@c.us', '').replace('@s.whatsapp.net', '')
                        # Formata número brasileiro (se começar com 55)
                        if phone_number.startswith('55') and len(phone_number) >= 12:
                            formatted = f"+{phone_number[:2]} ({phone_number[2:4]}) {phone_number[4:9]}-{phone_number[9:]}"
                            phone_number = formatted
                        else:
                            phone_number = f"+{phone_number}"
                
                # Considera conectado se realmente ready OU se está autenticado (processo de conexão)
                if connected or (is_authenticated and not has_qr):
                    return jsonify({
                        "connected": True, 
                        "message": "WhatsApp conectado" if connected else "WhatsApp conectando...",
                        "hasQr": False,
                        "port": whatsapp_port,
                        "phone_number": phone_number,
                        "isAuthenticated": is_authenticated,
                        "isConnecting": not connected and is_authenticated  # Conectando se autenticado mas não ready
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
    try:
        from web.utils.instance_helper import get_or_create_user_instance, get_whatsapp_server_url
        from web.utils.auth_helpers import get_current_user_id
        import requests
        
        # Obtém instância do usuário atual
        user_id = get_current_user_id() or 1
        data = request.get_json() or {}
        instance_id = data.get('instance_id')
        
        instance = get_or_create_user_instance(user_id, instance_id)
        if not instance:
            return jsonify({"success": False, "error": "Instância não encontrada"}), 404
        
        whatsapp_port = instance.get('port', 5001)
        server_url = get_whatsapp_server_url(whatsapp_port)
        
        # IMPORTANTE: Usa user_id_instance_id para identificar instância única
        # Isso permite múltiplas instâncias por usuário funcionarem independentemente
        from web.utils.instance_helper import get_instance_user_id
        unique_user_id = get_instance_user_id(user_id, instance.get('id', user_id))
        
        # Chama endpoint de desconexão do servidor Node.js
        try:
            response = requests.post(f"{server_url}/disconnect", json={"user_id": unique_user_id}, timeout=5)
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
@app.route('/api/ai-config', methods=['GET'])
def get_ai_config():
    """Obtém configuração da IA (do usuário logado)"""
    from web.utils.auth_helpers import get_current_user_id
    
    user_id = get_current_user_id()
    if not user_id and AUTH_REQUIRED:
        return jsonify({"error": "Usuário não autenticado"}), 401
    
    config = load_config(user_id)
    # Retorna configuração completa (API key mascarada para exibição)
    api_key = config.get('api_key', '')
    masked_key = api_key[:10] + '...' + api_key[-4:] if len(api_key) > 14 else '***' if api_key else ''
    
    return jsonify({
        'config': {
            'provider': config.get('provider', 'openai'),
            'api_key': masked_key,  # Mascarada para exibição
            'api_key_configured': bool(api_key),  # Indica se está configurada
            'model': config.get('model', 'gpt-4o-mini'),
            'system_prompt': config.get('system_prompt', 'Você é um assistente útil e amigável.')
        }
    })

@app.route('/api/ai/config', methods=['POST'])
@app.route('/api/ai-config', methods=['POST'])
@require_api_auth
def set_ai_config():
    """Configura a IA (salva por usuário)"""
    from web.utils.auth_helpers import get_current_user_id
    
    user_id = get_current_user_id()
    if not user_id and AUTH_REQUIRED:
        return jsonify({"success": False, "error": "Usuário não autenticado"}), 401
    
    data = request.get_json()
    
    # Carrega configuração atual do usuário (pode ter API key do .env)
    current_config = load_config(user_id)
    
    config = {
        'provider': data.get('provider', current_config.get('provider', 'openai')),
        'api_key': data.get('api_key') or current_config.get('api_key', ''),  # Se não enviar, mantém a do .env
        'model': data.get('model', current_config.get('model', 'gpt-4o-mini')),
        'system_prompt': data.get('system_prompt', current_config.get('system_prompt', 'Você é um assistente útil e amigável.'))
    }
    
    # Atualiza handler
    ai.set_config(
        provider=config['provider'],
        api_key=config['api_key'],
        model=config['model'],
        system_prompt=config['system_prompt']
    )
    
    # Salva configuração do usuário
    save_config(config, user_id)
    
    return jsonify({"success": True, "message": "Configuração salva!"})

@app.route('/api/ai/test', methods=['POST'])
@require_api_auth
def test_ai():
    """Testa a IA sem enviar mensagem real (apenas retorna resposta)"""
    try:
        from web.utils.auth_helpers import get_current_user_id
        
        user_id = get_current_user_id()
        if not user_id and AUTH_REQUIRED:
            return jsonify({"success": False, "error": "Usuário não autenticado"}), 401
        
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({"success": False, "error": "Mensagem não fornecida"}), 400
        
        # Carrega configuração do usuário
        config = load_config(user_id)
        if not config.get('api_key'):
            return jsonify({
                "success": False,
                "error": "IA não configurada. Configure a API Key primeiro."
            }), 400
        
        # Usa um número de teste fictício
        test_phone = "test_123456789"
        
        # Obtém resposta da IA (sem enviar mensagem real)
        try:
            response = ai.get_response(test_phone, message, tenant_id=None, instance_id=user_id)
            
            return jsonify({
                "success": True,
                "response": response,
                "note": "Esta é uma resposta de teste. Nenhuma mensagem foi enviada."
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Erro ao processar com IA: {str(e)}"
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

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
        
        # Verifica se resposta automática está habilitada
        AUTO_RESPOND = os.getenv('AUTO_RESPOND', 'false').lower() == 'true'
        
        if not AUTO_RESPOND:
            # Modo de teste: apenas registra a mensagem, não responde
            print(f"[📨] Mensagem recebida (MODO TESTE - sem resposta automática): {phone}: {message}")
            return jsonify({
                "success": True,
                "processed_by": "test_mode",
                "message": "Mensagem recebida mas resposta automática desabilitada",
                "note": "Para habilitar respostas automáticas, defina AUTO_RESPOND=true no .env"
            })
        
        # Fallback: Processa com IA (se fluxos não processaram)
        # Busca user_id a partir do instance_id (webhook não tem sessão)
        user_id = None
        if instance_id:
            # No modo simplificado, instance_id = user_id
            user_id = instance_id
        elif AUTH_REQUIRED:
            # Tenta pegar da sessão se disponível
            try:
                user_id = session.get('user_id')
            except:
                pass
        
        config = load_config(user_id)
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
    """Health check completo - verifica todas as dependências"""
    from config.settings import WHATSAPP_SERVER_URL, IS_PRODUCTION, DATABASE_URL
    from web.utils.http_client import get_with_retry
    
    health_status = {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }
    
    # Check 1: Banco de dados
    try:
        from src.database.db import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        health_status["checks"]["database"] = {"status": "ok"}
    except Exception as e:
        health_status["checks"]["database"] = {
            "status": "error",
            "message": str(e)[:100]  # Limita tamanho
        }
        health_status["status"] = "degraded"
        logger.warning(f"Health check: Database error - {e}")
    
    # Check 2: Servidor WhatsApp
    if IS_PRODUCTION and WHATSAPP_SERVER_URL and 'localhost' not in WHATSAPP_SERVER_URL:
        try:
            response = get_with_retry(f"{WHATSAPP_SERVER_URL}/health", timeout=5, max_retries=1)
            if response.status_code == 200:
                health_status["checks"]["whatsapp_server"] = {
                    "status": "ok",
                    "url": WHATSAPP_SERVER_URL
                }
            else:
                health_status["checks"]["whatsapp_server"] = {
                    "status": "error",
                    "message": f"Status {response.status_code}",
                    "url": WHATSAPP_SERVER_URL
                }
                health_status["status"] = "degraded"
                logger.warning(f"Health check: WhatsApp server returned {response.status_code}")
        except Exception as e:
            health_status["checks"]["whatsapp_server"] = {
                "status": "error",
                "message": str(e)[:100],
                "url": WHATSAPP_SERVER_URL
            }
            health_status["status"] = "degraded"
            logger.warning(f"Health check: WhatsApp server error - {e}")
    else:
        health_status["checks"]["whatsapp_server"] = {
            "status": "not_configured",
            "message": "WHATSAPP_SERVER_URL não configurado ou em modo desenvolvimento"
        }
    
    # Se algum check crítico falhou, retorna 503
    if health_status["status"] == "degraded":
        return jsonify(health_status), 503
    
    return jsonify(health_status), 200
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
    
    # Tenta iniciar servidor WhatsApp automaticamente (apenas em desenvolvimento)
    from config.settings import IS_PRODUCTION
    if whatsapp and not IS_PRODUCTION:
        try:
            print("[*] Iniciando servidor WhatsApp...")
            if whatsapp.start_server():
                print("[✓] Servidor WhatsApp iniciado com sucesso!")
            else:
                print("[!] Servidor WhatsApp pode não ter iniciado. Verifique os logs.")
        except Exception as e:
            print(f"[!] Erro ao iniciar servidor WhatsApp: {e}")
            print("[!] Você pode iniciar manualmente com: node whatsapp_server.js")
    elif IS_PRODUCTION:
        print("[*] Modo produção: Servidor WhatsApp deve ser iniciado como serviço separado no Railway")
    
    # Inicia worker de mensagens (aguarda um pouco para garantir que tudo está pronto)
    import time
    time.sleep(2)
    try:
        start_message_worker()
    except Exception as e:
        print(f"[!] Erro ao iniciar worker de mensagens: {e}")
    
    # Inicia Flask
    # Em produção, Railway define PORT automaticamente via variável de ambiente
    port = int(os.getenv('PORT', 5002))
    from config.settings import IS_PRODUCTION
    app.run(host='0.0.0.0', port=port, debug=not IS_PRODUCTION)

