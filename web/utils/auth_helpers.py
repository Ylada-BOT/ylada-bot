"""
Funções auxiliares para autenticação e autorização
"""
from flask import session
from src.database.db import SessionLocal
from src.models.user import User, UserRole
from src.models.tenant import Tenant
import logging

logger = logging.getLogger(__name__)


def get_current_user_id():
    """Obtém ID do usuário atual da sessão"""
    return session.get('user_id')


def get_current_user_role():
    """Obtém role do usuário atual da sessão"""
    return session.get('user_role', 'user')


def is_admin():
    """Verifica se o usuário atual é admin"""
    role = get_current_user_role()
    return role == 'admin' or role == UserRole.ADMIN.value


def get_current_tenant_id():
    """
    Obtém tenant_id do usuário atual
    
    Retorna:
    - tenant_id (int): ID do primeiro tenant do usuário
    - None: Se for admin ou não tiver tenant
    - None: Se não tiver usuário logado
    """
    user_id = get_current_user_id()
    if not user_id:
        return None
    
    # Admin pode ver todos os dados (retorna None para não filtrar)
    if is_admin():
        return None
    
    try:
        db = SessionLocal()
        try:
            # Busca primeiro tenant do usuário
            tenant = db.query(Tenant).filter(Tenant.user_id == user_id).first()
            if tenant:
                return tenant.id
            return None
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Erro ao obter tenant_id: {e}")
        return None


def get_user_tenants():
    """
    Obtém todos os tenants do usuário atual
    
    Retorna:
    - list: Lista de tenants do usuário
    - []: Se não tiver tenants ou não estiver logado
    """
    user_id = get_current_user_id()
    if not user_id:
        return []
    
    try:
        db = SessionLocal()
        try:
            tenants = db.query(Tenant).filter(Tenant.user_id == user_id).all()
            return tenants
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Erro ao obter tenants do usuário: {e}")
        return []




