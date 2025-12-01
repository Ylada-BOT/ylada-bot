"""
Sistema de Gerenciamento de Múltiplos Usuários/Atendentes
Similar ao Botconversa - permite vários atendentes no mesmo número
"""
from typing import Dict, List, Optional
from datetime import datetime
import json
import os
from pathlib import Path


class UsersManager:
    """Gerencia múltiplos usuários/atendentes"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.users_file = self.data_dir / "users.json"
        self.users = self._load_users()
    
    def _load_users(self) -> Dict:
        """Carrega usuários do arquivo"""
        if self.users_file.exists():
            try:
                with open(self.users_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_users(self):
        """Salva usuários no arquivo"""
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(self.users, f, indent=2, ensure_ascii=False)
    
    def create_user(self, username: str, email: str, role: str = "attendant") -> Dict:
        """
        Cria novo usuário/atendente
        
        Args:
            username: Nome do usuário
            email: Email do usuário
            role: Função (admin, attendant, viewer)
        
        Returns:
            Dict com dados do usuário criado
        """
        user_id = f"user_{len(self.users) + 1}"
        user = {
            "id": user_id,
            "username": username,
            "email": email,
            "role": role,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "active": True,
            "assigned_conversations": []
        }
        
        self.users[user_id] = user
        self._save_users()
        return user
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Obtém usuário por ID"""
        return self.users.get(user_id)
    
    def list_users(self, role: Optional[str] = None) -> List[Dict]:
        """Lista todos os usuários"""
        users_list = list(self.users.values())
        if role:
            users_list = [u for u in users_list if u.get("role") == role]
        return users_list
    
    def assign_conversation(self, user_id: str, phone: str) -> bool:
        """Atribui conversa a um atendente"""
        user = self.get_user(user_id)
        if not user:
            return False
        
        if phone not in user["assigned_conversations"]:
            user["assigned_conversations"].append(phone)
            self._save_users()
        return True
    
    def unassign_conversation(self, user_id: str, phone: str) -> bool:
        """Remove atribuição de conversa"""
        user = self.get_user(user_id)
        if not user:
            return False
        
        if phone in user["assigned_conversations"]:
            user["assigned_conversations"].remove(phone)
            self._save_users()
        return True
    
    def get_user_conversations(self, user_id: str) -> List[str]:
        """Retorna lista de conversas atribuídas ao usuário"""
        user = self.get_user(user_id)
        if not user:
            return []
        return user.get("assigned_conversations", [])
    
    def update_last_login(self, user_id: str):
        """Atualiza último login do usuário"""
        user = self.get_user(user_id)
        if user:
            user["last_login"] = datetime.now().isoformat()
            self._save_users()

