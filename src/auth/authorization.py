"""
Sistema de autorização (permissões)
"""
from functools import wraps
from flask import request, jsonify
from typing import Optional, Callable
from src.models.user import UserRole
from src.models.tenant import Tenant
from src.auth.authentication import verify_token
from src.database.db import get_db


def require_auth(f: Callable) -> Callable:
    """Decorator para exigir autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token não fornecido'}), 401
        
        # Remove "Bearer " se presente
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Token inválido ou expirado'}), 401
        
        # Adiciona user_id ao request
        request.user_id = payload['user_id']
        request.user_email = payload['email']
        request.user_role = payload['role']
        
        return f(*args, **kwargs)
    
    return decorated_function


def require_role(*allowed_roles: UserRole):
    """Decorator para exigir role específica"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        @require_auth
        def decorated_function(*args, **kwargs):
            user_role = UserRole(request.user_role)
            
            if user_role not in allowed_roles:
                return jsonify({'error': 'Acesso negado'}), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def get_current_tenant_id() -> Optional[int]:
    """Obtém tenant_id do usuário atual (primeiro tenant)"""
    if not hasattr(request, 'user_id'):
        return None
    
    db = next(get_db())
    try:
        from src.models.tenant import Tenant
        tenant = db.query(Tenant).filter(Tenant.user_id == request.user_id).first()
        return tenant.id if tenant else None
    finally:
        db.close()


def require_tenant_access(f: Callable) -> Callable:
    """Decorator para verificar acesso ao tenant"""
    @wraps(f)
    @require_auth
    def decorated_function(*args, **kwargs):
        tenant_id = kwargs.get('tenant_id') or request.json.get('tenant_id') if request.is_json else None
        
        if not tenant_id:
            return jsonify({'error': 'tenant_id não fornecido'}), 400
        
        # Verifica se usuário tem acesso ao tenant
        db = next(get_db())
        try:
            tenant = db.query(Tenant).filter(
                Tenant.id == tenant_id,
                Tenant.user_id == request.user_id
            ).first()
            
            if not tenant:
                return jsonify({'error': 'Acesso negado ao tenant'}), 403
            
            request.tenant_id = tenant_id
            return f(*args, **kwargs)
        finally:
            db.close()
    
    return decorated_function
