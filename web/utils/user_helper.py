"""
Helper para gerenciar usuários em modo simplificado (sem banco de dados)
Usa arquivo JSON para armazenar usuários
"""
import json
import os
import hashlib
from datetime import datetime
from typing import Optional, Dict


USERS_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'users.json')


def _load_users():
    """Carrega usuários do arquivo"""
    if not os.path.exists(USERS_FILE):
        return {}
    
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}
    except Exception as e:
        print(f"[!] Erro ao carregar usuários: {e}")
        return {}


def _save_users(users_data):
    """Salva usuários no arquivo"""
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[!] Erro ao salvar usuários: {e}")


def _hash_password(password: str) -> str:
    """Gera hash simples da senha (SHA256)"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def _verify_password(password: str, password_hash: str) -> bool:
    """Verifica senha"""
    return _hash_password(password) == password_hash


def get_next_user_id():
    """Obtém próximo ID de usuário disponível"""
    users = _load_users()
    if not users:
        return 1
    
    max_id = max(int(uid) for uid in users.keys() if uid.isdigit())
    return max_id + 1


def register_user_simple(email: str, password: str, name: str) -> Optional[Dict]:
    """
    Registra novo usuário (modo simplificado)
    
    Returns:
        dict: Dados do usuário criado ou None se email já existe
    """
    users = _load_users()
    
    # Verifica se email já existe
    for user_data in users.values():
        if user_data.get('email', '').lower() == email.lower():
            return None
    
    # Cria novo usuário
    user_id = get_next_user_id()
    user = {
        'id': user_id,
        'email': email.lower(),
        'password_hash': _hash_password(password),
        'name': name,
        'role': 'user',
        'is_active': True,
        'created_at': datetime.now().isoformat()
    }
    
    users[str(user_id)] = user
    _save_users(users)
    
    print(f"[✓] Usuário criado: {name} ({email}) - ID: {user_id}")
    
    # Retorna sem password_hash
    user_copy = user.copy()
    del user_copy['password_hash']
    return user_copy


def authenticate_user_simple(email: str, password: str) -> Optional[Dict]:
    """
    Autentica usuário (modo simplificado)
    
    Returns:
        dict: Dados do usuário ou None se credenciais inválidas
    """
    users = _load_users()
    
    # Busca usuário por email
    for user_data in users.values():
        if user_data.get('email', '').lower() == email.lower():
            # Verifica senha
            if _verify_password(password, user_data.get('password_hash', '')):
                # Retorna sem password_hash
                user_copy = user_data.copy()
                del user_copy['password_hash']
                return user_copy
    
    return None


def get_user_by_id_simple(user_id: int) -> Optional[Dict]:
    """Obtém usuário por ID"""
    users = _load_users()
    user = users.get(str(user_id))
    
    if user:
        user_copy = user.copy()
        if 'password_hash' in user_copy:
            del user_copy['password_hash']
        return user_copy
    
    return None

