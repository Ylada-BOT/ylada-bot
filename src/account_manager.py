"""
Gerenciador de Contas (Multi-tenancy)
Isola dados por conta
"""
from typing import Dict, List, Optional
import uuid


class AccountManager:
    """Gerencia contas (multi-tenancy)"""
    
    def __init__(self, db):
        """
        Inicializa gerenciador
        
        Args:
            db: Instância de Database
        """
        self.db = db
    
    def create_account(self, name: str, phone: str, plan: str = 'owner') -> Dict:
        """
        Cria nova conta
        
        Args:
            name: Nome da conta
            phone: Número do WhatsApp
            plan: Plano (owner, free, basic, pro)
            
        Returns:
            Dados da conta criada
        """
        account = {
            'id': str(uuid.uuid4()),
            'name': name,
            'phone': phone,
            'plan': plan,
            'status': 'active'
        }
        
        return self.db.create_account(account)
    
    def get_account(self, account_id: str) -> Optional[Dict]:
        """
        Retorna dados da conta
        
        Args:
            account_id: ID da conta
            
        Returns:
            Dados da conta ou None
        """
        return self.db.get_account(account_id)
    
    def get_account_by_phone(self, phone: str) -> Optional[Dict]:
        """
        Retorna conta pelo telefone
        
        Args:
            phone: Número do WhatsApp
            
        Returns:
            Dados da conta ou None
        """
        return self.db.get_account_by_phone(phone)
    
    def get_all_accounts(self) -> List[Dict]:
        """
        Retorna todas as contas
        
        Returns:
            Lista de contas
        """
        return self.db.get_all_accounts()
    
    def get_account_contacts(self, account_id: str) -> List[Dict]:
        """
        Retorna contatos da conta (isolado)
        
        Args:
            account_id: ID da conta
            
        Returns:
            Lista de contatos
        """
        return self.db.get_contacts_by_account(account_id)
    
    def get_account_campaigns(self, account_id: str) -> List[Dict]:
        """
        Retorna campanhas da conta (isolado)
        
        Args:
            account_id: ID da conta
            
        Returns:
            Lista de campanhas
        """
        return self.db.get_campaigns_by_account(account_id)
    
    def get_account_conversations(self, account_id: str, limit: int = 100) -> List[Dict]:
        """
        Retorna conversas da conta (isolado)
        
        Args:
            account_id: ID da conta
            limit: Limite de conversas
            
        Returns:
            Lista de conversas
        """
        return self.db.get_conversations_by_account(account_id, limit)
    
    def create_contact(self, account_id: str, phone: str, name: Optional[str] = None, tags: Optional[List[str]] = None) -> Dict:
        """
        Cria contato na conta
        
        Args:
            account_id: ID da conta
            phone: Número do contato
            name: Nome do contato
            tags: Tags do contato
            
        Returns:
            Dados do contato criado
        """
        contact = {
            'account_id': account_id,
            'phone': phone,
            'name': name,
            'tags': tags or []
        }
        
        return self.db.create_contact(contact)
    
    def create_campaign(self, account_id: str, name: str, message: Optional[str] = None, 
                       qr_code_url: Optional[str] = None, link: Optional[str] = None) -> Dict:
        """
        Cria campanha na conta
        
        Args:
            account_id: ID da conta
            name: Nome da campanha
            message: Mensagem da campanha
            qr_code_url: URL do QR Code
            link: Link da campanha
            
        Returns:
            Dados da campanha criada
        """
        campaign = {
            'account_id': account_id,
            'name': name,
            'message': message,
            'qr_code_url': qr_code_url,
            'link': link
        }
        
        return self.db.create_campaign(campaign)
    
    def create_conversation(self, account_id: str, contact_id: Optional[str], 
                           message: str, from_me: bool = False) -> Dict:
        """
        Cria conversa/mensagem na conta
        
        Args:
            account_id: ID da conta
            contact_id: ID do contato (opcional)
            message: Mensagem
            from_me: Se a mensagem foi enviada por você
            
        Returns:
            Dados da conversa criada
        """
        conversation = {
            'account_id': account_id,
            'contact_id': contact_id,
            'message': message,
            'from_me': from_me
        }
        
        return self.db.create_conversation(conversation)

