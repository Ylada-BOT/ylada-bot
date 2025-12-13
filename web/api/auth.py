"""
Rotas de autenticação
"""
from flask import Blueprint, request, jsonify
import os

# Tenta importar banco de dados, mas não falha se não estiver configurado
try:
    from sqlalchemy.orm import Session
    from src.database.db import SessionLocal
    from src.auth.authentication import (
        register_user, authenticate_user, create_token, get_user_by_id
    )
    from src.models.user import UserRole
    DB_AVAILABLE = True
except Exception as e:
    # Modo desenvolvimento sem banco de dados
    DB_AVAILABLE = False
    print(f"[!] Banco de dados não disponível: {e}")
    print("[!] Sistema funcionará em modo básico (sem autenticação persistente)")

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/register', methods=['POST'])
def register():
    """Registra novo usuário"""
    if not DB_AVAILABLE:
        return jsonify({
            'error': 'Banco de dados não configurado. Configure PostgreSQL e rode: python scripts/init_db.py'
        }), 503
    
    try:
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if not email or not password or not name:
            return jsonify({'error': 'Email, senha e nome são obrigatórios'}), 400
        
        db = SessionLocal()
        try:
            user = register_user(db, email, password, name, UserRole.USER)
            
            if not user:
                return jsonify({'error': 'Email já cadastrado'}), 400
            
            # Cria token
            token = create_token(user.id, user.email, user.role.value)
            
            # Salva na sessão (para uso no Flask)
            from flask import session
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_role'] = user.role.value
            
            return jsonify({
                'success': True,
                'message': 'Usuário criado com sucesso',
                'token': token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'role': user.role.value
                }
            }), 201
        finally:
            db.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/login', methods=['POST'])
def login():
    """Login de usuário"""
    if not DB_AVAILABLE:
        return jsonify({
            'error': 'Banco de dados não configurado. Configure PostgreSQL e rode: python scripts/init_db.py'
        }), 503
    
    try:
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        db = SessionLocal()
        try:
            user = authenticate_user(db, email, password)
            
            if not user:
                return jsonify({'error': 'Credenciais inválidas'}), 401
            
            # Cria token
            token = create_token(user.id, user.email, user.role.value)
            
            # Salva na sessão (para uso no Flask)
            from flask import session
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_role'] = user.role.value
            
            return jsonify({
                'success': True,
                'token': token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'role': user.role.value
                }
            }), 200
        finally:
            db.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/me', methods=['GET'])
def get_current_user():
    """Obtém usuário atual"""
    from src.auth.authorization import require_auth
    
    @require_auth
    def _get_user():
        db = SessionLocal()
        try:
            user = get_user_by_id(db, request.user_id)
            
            if not user:
                return jsonify({'error': 'Usuário não encontrado'}), 404
            
            return jsonify({
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'role': user.role.value,
                'is_active': user.is_active
            }), 200
        finally:
            db.close()
    
    return _get_user()
