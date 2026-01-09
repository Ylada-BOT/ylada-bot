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
        print(f"[!] Arquivo de usuários não encontrado: {USERS_FILE}")
        # Cria arquivo vazio se não existir
        try:
            os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            print(f"[✓] Arquivo de usuários criado: {USERS_FILE}")
            return {}
        except Exception as create_error:
            print(f"[!] Erro ao criar arquivo de usuários: {create_error}")
            return {}
    
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            users = json.load(f)
            print(f"[✓] Usuários carregados: {len(users)} usuário(s)")
            return users
    except json.JSONDecodeError as e:
        print(f"[!] Erro ao decodificar JSON: {e}")
        # Tenta criar arquivo novo se JSON está corrompido
        try:
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            print(f"[✓] Arquivo JSON recriado após erro de decodificação")
        except:
            pass
        return {}
    except Exception as e:
        print(f"[!] Erro ao carregar usuários: {e}")
        import traceback
        print(f"[!] Traceback: {traceback.format_exc()}")
        return {}


def _save_users(users_data):
    """Salva usuários no arquivo"""
    try:
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        # Garante que o diretório tem permissões corretas
        os.chmod(os.path.dirname(USERS_FILE), 0o755)
        
        # Salva arquivo
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, indent=2, ensure_ascii=False)
        
        # Garante permissões de leitura/escrita
        try:
            os.chmod(USERS_FILE, 0o644)
        except:
            pass
        
        print(f"[✓] Usuários salvos em {USERS_FILE}")
        print(f"[✓] Total de usuários: {len(users_data)}")
    except Exception as e:
        print(f"[!] Erro ao salvar usuários: {e}")
        import traceback
        print(f"[!] Traceback: {traceback.format_exc()}")


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
    
    # Verifica se foi salvo corretamente
    saved_users = _load_users()
    if str(user_id) not in saved_users:
        print(f"[!] AVISO: Usuário não foi salvo corretamente!")
    else:
        print(f"[✓] Usuário criado e verificado: {name} ({email}) - ID: {user_id}")
        print(f"[✓] Hash da senha: {user['password_hash'][:20]}...")
    
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
    
    if not users:
        print(f"[!] Nenhum usuário encontrado no arquivo")
        return None
    
    email_lower = email.lower().strip()
    print(f"[DEBUG AUTH] Buscando usuário com email: {email_lower}")
    print(f"[DEBUG AUTH] Total de usuários no arquivo: {len(users)}")
    
    # Busca usuário por email
    for user_id, user_data in users.items():
        user_email = user_data.get('email', '').lower().strip()
        print(f"[DEBUG AUTH] Verificando usuário ID {user_id}: {user_email}")
        
        if user_email == email_lower:
            print(f"[DEBUG AUTH] Email encontrado! Verificando senha...")
            # Verifica senha
            password_hash = user_data.get('password_hash', '')
            if not password_hash:
                print(f"[!] Usuário {email} não tem hash de senha")
                return None
            
            # Gera hash da senha fornecida para comparar
            provided_hash = _hash_password(password)
            print(f"[DEBUG AUTH] Hash fornecido: {provided_hash[:20]}...")
            print(f"[DEBUG AUTH] Hash armazenado: {password_hash[:20]}...")
            
            if _verify_password(password, password_hash):
                # Retorna sem password_hash
                user_copy = user_data.copy()
                if 'password_hash' in user_copy:
                    del user_copy['password_hash']
                print(f"[✓] Usuário autenticado: {email}")
                return user_copy
            else:
                print(f"[!] Senha incorreta para {email}")
                print(f"[DEBUG AUTH] Hash não corresponde")
                return None
    
    print(f"[!] Email não encontrado: {email}")
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








