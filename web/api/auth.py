"""
Rotas de autenticação
"""
from flask import Blueprint, request, jsonify, session
import os
import jwt
from datetime import datetime, timedelta

# Tenta importar banco de dados, mas não falha se não estiver configurado
DB_AVAILABLE = False
try:
    from sqlalchemy.orm import Session
    from src.database.db import SessionLocal
    from src.auth.authentication import (
        register_user, authenticate_user, create_token, get_user_by_id
    )
    from src.models.user import UserRole
    # Testa conexão antes de marcar como disponível
    try:
        db = SessionLocal()
        db.close()
        DB_AVAILABLE = True
        print("[✓] Banco de dados disponível")
    except Exception as db_error:
        DB_AVAILABLE = False
        print(f"[!] Banco de dados não disponível (erro de conexão): {db_error}")
        print("[!] Sistema funcionará em modo simplificado (arquivo JSON)")
except Exception as e:
    # Modo desenvolvimento sem banco de dados
    DB_AVAILABLE = False
    print(f"[!] Banco de dados não disponível: {e}")
    print("[!] Sistema funcionará em modo simplificado (arquivo JSON)")

# Importa helpers simplificados
try:
    from web.utils.user_helper import (
        register_user_simple, authenticate_user_simple, get_user_by_id_simple
    )
    SIMPLE_AUTH_AVAILABLE = True
except Exception as e:
    SIMPLE_AUTH_AVAILABLE = False
    print(f"[!] Helpers simplificados não disponíveis: {e}")

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Configuração JWT simples
JWT_SECRET = os.getenv('JWT_SECRET', 'dev-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


def create_token_simple(user_id: int, email: str, role: str) -> str:
    """Cria token JWT simples"""
    payload = {
        'user_id': user_id,
        'email': email,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


@bp.route('/setup', methods=['POST'])
def setup_first_user():
    """Cria primeiro usuário do sistema (apenas se não houver usuários)"""
    try:
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        name = data.get('name', 'Admin')
        
        if not email or not password:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        # Verifica se já existe usuário
        if SIMPLE_AUTH_AVAILABLE:
            users = _load_users()
            if users:
                return jsonify({'error': 'Sistema já possui usuários. Use /register para criar novos.'}), 400
            
            # Cria primeiro usuário
            user = register_user_simple(email, password, name)
            if user:
                token = create_token_simple(user['id'], user['email'], user['role'])
                session['user_id'] = user['id']
                session['user_email'] = user['email']
                session['user_role'] = user['role']
                
                return jsonify({
                    'success': True,
                    'message': 'Primeiro usuário criado com sucesso!',
                    'token': token,
                    'user': user
                }), 201
        
        return jsonify({'error': 'Sistema de autenticação não disponível'}), 503
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def _load_users():
    """Carrega usuários do arquivo (helper interno)"""
    if not SIMPLE_AUTH_AVAILABLE:
        return {}
    try:
        from web.utils.user_helper import authenticate_user_simple
        # Tenta carregar arquivo diretamente
        import json
        import os
        users_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'users.json')
        if os.path.exists(users_file):
            with open(users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {}


@bp.route('/register', methods=['POST'])
def register():
    """Registra novo usuário"""
    try:
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if not email or not password or not name:
            return jsonify({'error': 'Email, senha e nome são obrigatórios'}), 400
        
        # Tenta usar banco de dados se disponível
        if DB_AVAILABLE:
            db = SessionLocal()
            try:
                user = register_user(db, email, password, name, UserRole.USER)
                
                if not user:
                    return jsonify({'error': 'Email já cadastrado'}), 400
                
                # Cria token
                token = create_token(user.id, user.email, user.role.value)
                
                # Salva na sessão
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
        
        # Modo simplificado (arquivo JSON)
        elif SIMPLE_AUTH_AVAILABLE:
            user = register_user_simple(email, password, name)
            
            if not user:
                return jsonify({'error': 'Email já cadastrado'}), 400
            
            # Cria token
            token = create_token_simple(user['id'], user['email'], user['role'])
            
            # Salva na sessão
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_role'] = user['role']
            
            return jsonify({
                'success': True,
                'message': 'Usuário criado com sucesso',
                'token': token,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'name': user['name'],
                    'role': user['role']
                }
            }), 201
        
        else:
            return jsonify({
                'error': 'Sistema de autenticação não disponível'
            }), 503
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/login', methods=['POST'])
def login():
    """Login de usuário"""
    try:
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        # Tenta usar banco de dados se disponível
        if DB_AVAILABLE:
            try:
                db = SessionLocal()
                try:
                    user = authenticate_user(db, email, password)
                    
                    if not user:
                        # Se não encontrou no banco, tenta modo simplificado
                        if SIMPLE_AUTH_AVAILABLE:
                            user = authenticate_user_simple(email, password)
                            if not user:
                                return jsonify({'error': 'Credenciais inválidas'}), 401
                            
                            # Cria token simplificado
                            token = create_token_simple(user['id'], user['email'], user['role'])
                            session['user_id'] = user['id']
                            session['user_email'] = user['email']
                            session['user_role'] = user['role']
                            
                            return jsonify({
                                'success': True,
                                'token': token,
                                'user': {
                                    'id': user['id'],
                                    'email': user['email'],
                                    'name': user['name'],
                                    'role': user['role']
                                }
                            }), 200
                        return jsonify({'error': 'Credenciais inválidas'}), 401
                    
                    # Cria token
                    token = create_token(user.id, user.email, user.role.value)
                    
                    # Salva na sessão
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
            except Exception as db_error:
                # Se erro de conexão, usa modo simplificado como fallback
                print(f"[!] Erro ao conectar com banco: {db_error}")
                if SIMPLE_AUTH_AVAILABLE:
                    user = authenticate_user_simple(email, password)
                    if not user:
                        return jsonify({'error': 'Credenciais inválidas'}), 401
                    
                    token = create_token_simple(user['id'], user['email'], user['role'])
                    session['user_id'] = user['id']
                    session['user_email'] = user['email']
                    session['user_role'] = user['role']
                    
                    return jsonify({
                        'success': True,
                        'token': token,
                        'user': {
                            'id': user['id'],
                            'email': user['email'],
                            'name': user['name'],
                            'role': user['role']
                        }
                    }), 200
                else:
                    return jsonify({
                        'error': f'Erro de conexão com banco de dados: {str(db_error)}'
                    }), 503
        
        # Modo simplificado (arquivo JSON)
        elif SIMPLE_AUTH_AVAILABLE:
            user = authenticate_user_simple(email, password)
            
            if not user:
                return jsonify({'error': 'Credenciais inválidas'}), 401
            
            # Cria token
            token = create_token_simple(user['id'], user['email'], user['role'])
            
            # Salva na sessão
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_role'] = user['role']
            
            return jsonify({
                'success': True,
                'token': token,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'name': user['name'],
                    'role': user['role']
                }
            }), 200
        
        else:
            return jsonify({
                'error': 'Sistema de autenticação não disponível'
            }), 503
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/me', methods=['GET'])
def get_current_user():
    """Obtém usuário atual"""
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'Usuário não autenticado'}), 401
    
    # Tenta usar banco de dados se disponível
    if DB_AVAILABLE:
        try:
            db = SessionLocal()
            try:
                user = get_user_by_id(db, user_id)
                
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
        except:
            pass
    
    # Modo simplificado (arquivo JSON)
    if SIMPLE_AUTH_AVAILABLE:
        user = get_user_by_id_simple(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({
            'id': user['id'],
            'email': user['email'],
            'name': user['name'],
            'role': user['role'],
            'is_active': user.get('is_active', True)
        }), 200
    
    return jsonify({'error': 'Sistema de autenticação não disponível'}), 503
