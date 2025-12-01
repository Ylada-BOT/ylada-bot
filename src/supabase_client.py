"""
Cliente Supabase para Ylada BOT
"""
import os
from typing import List, Dict, Optional
from supabase import create_client, Client

class SupabaseClient:
    """Cliente para interagir com Supabase"""
    
    def __init__(self):
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            print("[!] Supabase não configurado. Usando armazenamento local.")
            self.client = None
            return
        
        try:
            self.client: Client = create_client(supabase_url, supabase_key)
            print("[✓] Supabase conectado")
        except Exception as e:
            print(f"[!] Erro ao conectar Supabase: {e}")
            self.client = None
    
    def is_connected(self) -> bool:
        """Verifica se está conectado"""
        return self.client is not None
    
    # ========== CONTATOS ==========
    
    def get_contacts(self, search: Optional[str] = None) -> List[Dict]:
        """Busca contatos"""
        if not self.client:
            return []
        
        try:
            query = self.client.table('contacts').select('*')
            
            if search:
                query = query.or_(f"name.ilike.%{search}%,phone.ilike.%{search}%")
            
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"[!] Erro ao buscar contatos: {e}")
            return []
    
    def add_contact(self, phone: str, name: str, **kwargs) -> bool:
        """Adiciona contato"""
        if not self.client:
            return False
        
        try:
            data = {
                'phone': phone,
                'name': name,
                **kwargs
            }
            self.client.table('contacts').insert(data).execute()
            return True
        except Exception as e:
            print(f"[!] Erro ao adicionar contato: {e}")
            return False
    
    def update_contact(self, phone: str, **kwargs) -> bool:
        """Atualiza contato"""
        if not self.client:
            return False
        
        try:
            self.client.table('contacts').update(kwargs).eq('phone', phone).execute()
            return True
        except Exception as e:
            print(f"[!] Erro ao atualizar contato: {e}")
            return False
    
    # ========== CONVERSAS ==========
    
    def add_message(self, phone: str, message: str, from_me: bool = False, **kwargs) -> bool:
        """Adiciona mensagem"""
        if not self.client:
            return False
        
        try:
            data = {
                'phone': phone,
                'message': message,
                'from_me': from_me,
                **kwargs
            }
            self.client.table('conversations').insert(data).execute()
            return True
        except Exception as e:
            print(f"[!] Erro ao adicionar mensagem: {e}")
            return False
    
    def get_messages(self, phone: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """Busca mensagens"""
        if not self.client:
            return []
        
        try:
            query = self.client.table('conversations').select('*').order('timestamp', desc=True).limit(limit)
            
            if phone:
                query = query.eq('phone', phone)
            
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"[!] Erro ao buscar mensagens: {e}")
            return []
    
    # ========== CAMPANHAS ==========
    
    def get_campaigns(self) -> List[Dict]:
        """Busca campanhas"""
        if not self.client:
            return []
        
        try:
            response = self.client.table('campaigns').select('*').order('created_at', desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"[!] Erro ao buscar campanhas: {e}")
            return []
    
    def create_campaign(self, name: str, message: str, **kwargs) -> Optional[Dict]:
        """Cria campanha"""
        if not self.client:
            return None
        
        try:
            data = {
                'name': name,
                'message': message,
                **kwargs
            }
            response = self.client.table('campaigns').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"[!] Erro ao criar campanha: {e}")
            return None

