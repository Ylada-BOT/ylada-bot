"""
Rate Limiting para proteger APIs e evitar bloqueios do WhatsApp

Limites do WhatsApp:
- ~20 mensagens/minuto por número
- ~1000 mensagens/dia por número
- Bloqueios podem ocorrer se exceder
"""
try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    FLASK_LIMITER_AVAILABLE = True
except ImportError:
    FLASK_LIMITER_AVAILABLE = False
    # Cria mock do Limiter se não estiver disponível
    class Limiter:
        def __init__(self, *args, **kwargs):
            pass
        def limit(self, *args, **kwargs):
            def decorator(f):
                return f
            return decorator

from flask import request, session, g
from functools import wraps
import logging

logger = logging.getLogger(__name__)

# Limiter será inicializado no app.py
limiter = None


def get_rate_limit_key():
    """
    Obtém chave única para rate limiting
    
    Prioridade:
    1. user_id da sessão (se logado)
    2. tenant_id (se disponível)
    3. IP do cliente
    """
    # Tenta obter user_id da sessão
    user_id = session.get('user_id')
    if user_id:
        tenant_id = session.get('tenant_id')
        if tenant_id:
            return f"user:{user_id}:tenant:{tenant_id}"
        return f"user:{user_id}"
    
    # Fallback para IP
    if FLASK_LIMITER_AVAILABLE:
        return get_remote_address()
    else:
        # Fallback simples se flask-limiter não disponível
        return request.remote_addr if hasattr(request, 'remote_addr') else 'default'


def get_whatsapp_rate_limits():
    """
    Retorna limites específicos para WhatsApp
    
    Limites conservadores para evitar bloqueios:
    - 15 mensagens/minuto (abaixo do limite de 20)
    - 800 mensagens/dia (abaixo do limite de 1000)
    """
    return [
        "15 per minute",  # Limite por minuto (conservador)
        "800 per day"     # Limite por dia (conservador)
    ]


def rate_limit_whatsapp(f):
    """
    Decorator para aplicar rate limiting em rotas de envio de WhatsApp
    
    Aplica limites específicos do WhatsApp:
    - 15 mensagens/minuto
    - 800 mensagens/dia
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if limiter is None:
            # Se limiter não foi inicializado, permite (modo dev)
            return f(*args, **kwargs)
        # Aplica limite
        return limiter.limit(get_whatsapp_rate_limits())(f)(*args, **kwargs)
    return decorated_function


def rate_limit_by_plan(f):
    """
    Decorator para aplicar rate limiting baseado no plano do tenant
    
    Limites por plano:
    - Free: 10 msg/min, 500 msg/dia
    - Basic: 15 msg/min, 2000 msg/dia
    - Pro: 20 msg/min, 10000 msg/dia
    - Enterprise: 50 msg/min, ilimitado
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtém plano do tenant (se disponível)
        tenant_id = session.get('tenant_id')
        plan = get_tenant_plan(tenant_id)
        
        # Aplica limites baseados no plano
        limits = get_plan_limits(plan)
        limiter.limit(limits)(f)(*args, **kwargs)
        
        return f(*args, **kwargs)
    return decorated_function


def get_tenant_plan(tenant_id):
    """
    Obtém plano do tenant (simplificado - pode melhorar depois)
    """
    if not tenant_id:
        return 'free'
    
    try:
        from src.database.db import SessionLocal
        from src.models.tenant import Tenant
        
        db = SessionLocal()
        try:
            tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
            if tenant and tenant.plan:
                return tenant.plan.name.lower() if hasattr(tenant.plan, 'name') else 'free'
            return 'free'
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Erro ao obter plano do tenant: {e}")
        return 'free'


def get_plan_limits(plan_name):
    """
    Retorna limites de rate limiting baseados no plano
    """
    limits = {
        'free': ["10 per minute", "500 per day"],
        'grátis': ["10 per minute", "500 per day"],
        'basic': ["15 per minute", "2000 per day"],
        'básico': ["15 per minute", "2000 per day"],
        'pro': ["20 per minute", "10000 per day"],
        'profissional': ["20 per minute", "10000 per day"],
        'enterprise': ["50 per minute"],  # Sem limite diário
    }
    
    return limits.get(plan_name.lower(), limits['free'])


def init_rate_limiter(app, redis_url=None):
    """
    Inicializa rate limiter no app Flask
    
    Args:
        app: Flask app
        redis_url: URL do Redis (opcional, usa memória se não fornecido)
    """
    global limiter
    
    # Configura storage (Redis se disponível, senão memória)
    if redis_url:
        try:
            limiter = Limiter(
                app=app,
                key_func=get_rate_limit_key,
                default_limits=["200 per hour"],
                storage_uri=redis_url,
                strategy="fixed-window"
            )
            logger.info("✅ Rate limiter configurado com Redis")
        except Exception as e:
            logger.warning(f"⚠️ Erro ao configurar Redis, usando memória: {e}")
            limiter = Limiter(
                app=app,
                key_func=get_rate_limit_key,
                default_limits=["200 per hour"],
                storage_uri="memory://",
                strategy="fixed-window"
            )
    else:
        limiter = Limiter(
            app=app,
            key_func=get_rate_limit_key,
            default_limits=["200 per hour"],
            storage_uri="memory://",
            strategy="fixed-window"
        )
        logger.info("✅ Rate limiter configurado com memória (use Redis para produção)")
    
    return limiter

