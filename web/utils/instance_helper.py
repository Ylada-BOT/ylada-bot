"""
Helper para gerenciar instância única por usuário
No modo simplificado: 1 usuário = 1 instância WhatsApp
"""
import json
import os
from datetime import datetime
from web.utils.auth_helpers import get_current_user_id


def get_or_create_user_instance(user_id=None):
    """
    Obtém ou cria automaticamente a instância do usuário
    
    No modo simplificado: cada usuário tem apenas 1 instância
    Se não existir, cria automaticamente
    
    Returns:
        dict: Dados da instância do usuário
    """
    if not user_id:
        user_id = get_current_user_id() or 1  # Default para desenvolvimento
    
    # MODO SIMPLES: Usa arquivo JSON
    instances_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'user_instances.json')
    os.makedirs(os.path.dirname(instances_file), exist_ok=True)
    
    # Carrega instâncias existentes
    user_instances = {}
    if os.path.exists(instances_file):
        try:
            with open(instances_file, 'r', encoding='utf-8') as f:
                user_instances = json.load(f)
        except:
            user_instances = {}
    
    # Verifica se usuário já tem instância
    user_key = str(user_id)
    if user_key in user_instances:
        return user_instances[user_key]
    
    # Cria nova instância para o usuário
    # Calcula porta baseada no user_id (5001, 5002, 5003...)
    base_port = 5001 + (user_id - 1)
    
    new_instance = {
        'id': user_id,  # ID da instância = ID do usuário (simplificado)
        'user_id': user_id,
        'name': f'Meu WhatsApp',
        'status': 'disconnected',
        'port': base_port,
        'phone_number': None,
        'agent_id': None,
        'messages_sent': 0,
        'messages_received': 0,
        'created_at': datetime.now().isoformat(),
        'session_dir': f"data/sessions/user_{user_id}"
    }
    
    # Salva instância
    user_instances[user_key] = new_instance
    with open(instances_file, 'w', encoding='utf-8') as f:
        json.dump(user_instances, f, indent=2, ensure_ascii=False)
    
    return new_instance


def get_user_instance_id(user_id=None):
    """
    Obtém ID da instância do usuário
    
    Returns:
        int: ID da instância do usuário
    """
    instance = get_or_create_user_instance(user_id)
    return instance.get('id')


def update_user_instance(user_id, updates):
    """
    Atualiza dados da instância do usuário
    
    Args:
        user_id: ID do usuário
        updates: Dict com campos para atualizar
    """
    instances_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'user_instances.json')
    
    user_instances = {}
    if os.path.exists(instances_file):
        try:
            with open(instances_file, 'r', encoding='utf-8') as f:
                user_instances = json.load(f)
        except:
            user_instances = {}
    
    user_key = str(user_id)
    if user_key in user_instances:
        user_instances[user_key].update(updates)
        user_instances[user_key]['updated_at'] = datetime.now().isoformat()
        
        with open(instances_file, 'w', encoding='utf-8') as f:
            json.dump(user_instances, f, indent=2, ensure_ascii=False)




