"""
Gerenciador de Múltiplas Instâncias WhatsApp
Suporta 4+ telefones simultaneamente
"""
from typing import Dict, List, Optional
from whatsapp_webjs_handler import WhatsAppWebJSHandler
import threading
import time


class InstanceManager:
    """Gerencia múltiplas instâncias WhatsApp"""
    
    def __init__(self, db):
        """
        Inicializa gerenciador
        
        Args:
            db: Instância de Database
        """
        self.db = db
        self.instances: Dict[str, Dict] = {}  # {instance_id: {'handler': handler, 'data': data}}
        self._load_instances()
        self._monitor_thread = None
        self._monitoring = False
    
    def _load_instances(self):
        """Carrega instâncias do banco de dados"""
        instances_data = self.db.get_all_instances()
        for inst_data in instances_data:
            instance_id = inst_data['id']
            handler = WhatsAppWebJSHandler(
                instance_name=inst_data['instance_name'],
                port=inst_data['port']
            )
            self.instances[instance_id] = {
                'handler': handler,
                'data': inst_data
            }
        print(f"[✓] {len(self.instances)} instâncias carregadas")
    
    def get_instance(self, account_id: str) -> Optional[WhatsAppWebJSHandler]:
        """
        Retorna handler da instância da conta
        
        Args:
            account_id: ID da conta
            
        Returns:
            Handler da instância ou None
        """
        instance_data = self.db.get_instance_by_account(account_id)
        if instance_data:
            instance_id = instance_data['id']
            if instance_id in self.instances:
                return self.instances[instance_id]['handler']
        return None
    
    def get_instance_by_id(self, instance_id: str) -> Optional[WhatsAppWebJSHandler]:
        """Retorna handler por ID da instância"""
        if instance_id in self.instances:
            return self.instances[instance_id]['handler']
        return None
    
    def start_instance(self, account_id: str) -> bool:
        """
        Inicia instância da conta
        
        Args:
            account_id: ID da conta
            
        Returns:
            True se iniciado com sucesso
        """
        handler = self.get_instance(account_id)
        if handler:
            success = handler.start_server()
            if success:
                self.db.update_instance_status(
                    self._get_instance_id_by_account(account_id),
                    'connecting'
                )
            return success
        return False
    
    def stop_instance(self, account_id: str) -> bool:
        """Para instância da conta"""
        handler = self.get_instance(account_id)
        if handler:
            handler.stop_server()
            instance_id = self._get_instance_id_by_account(account_id)
            if instance_id:
                self.db.update_instance_status(instance_id, 'disconnected')
            return True
        return False
    
    def get_all_instances_status(self) -> List[Dict]:
        """
        Retorna status de todas as instâncias
        
        Returns:
            Lista com status de cada instância
        """
        status_list = []
        for instance_id, instance_info in self.instances.items():
            handler = instance_info['handler']
            data = instance_info['data']
            
            is_ready = handler.is_ready()
            qr_code = None
            if not is_ready:
                qr_code = handler.get_qr_code()
            
            status_list.append({
                'id': instance_id,
                'account_id': data['account_id'],
                'instance_name': data['instance_name'],
                'port': data['port'],
                'status': 'connected' if is_ready else ('connecting' if qr_code else 'disconnected'),
                'qr_code': qr_code,
                'ready': is_ready
            })
        
        return status_list
    
    def get_instance_status(self, account_id: str) -> Optional[Dict]:
        """Retorna status da instância da conta"""
        instance_data = self.db.get_instance_by_account(account_id)
        if not instance_data:
            return None
        
        instance_id = instance_data['id']
        if instance_id not in self.instances:
            return None
        
        handler = self.instances[instance_id]['handler']
        is_ready = handler.is_ready()
        qr_code = None
        if not is_ready:
            qr_code = handler.get_qr_code()
        
        return {
            'id': instance_id,
            'account_id': account_id,
            'instance_name': instance_data['instance_name'],
            'port': instance_data['port'],
            'status': 'connected' if is_ready else ('connecting' if qr_code else 'disconnected'),
            'qr_code': qr_code,
            'ready': is_ready
        }
    
    def send_message(self, account_id: str, phone: str, message: str) -> bool:
        """
        Envia mensagem via instância da conta
        
        Args:
            account_id: ID da conta
            phone: Número do destinatário
            message: Mensagem
            
        Returns:
            True se enviado com sucesso
        """
        handler = self.get_instance(account_id)
        if not handler:
            print(f"[!] Instância não encontrada para conta {account_id}")
            return False
        
        if not handler.is_ready():
            print(f"[!] WhatsApp não está conectado para conta {account_id}")
            return False
        
        success = handler.send_message(phone, message)
        return success
    
    def get_chats(self, account_id: str) -> List[Dict]:
        """Retorna chats da instância da conta"""
        handler = self.get_instance(account_id)
        if not handler:
            return []
        
        if not handler.is_ready():
            return []
        
        return handler.get_chats()
    
    def get_chat_messages(self, account_id: str, chat_id: str, limit: int = 50) -> List[Dict]:
        """Retorna mensagens de um chat"""
        handler = self.get_instance(account_id)
        if not handler:
            return []
        
        if not handler.is_ready():
            return []
        
        return handler.get_chat_messages(chat_id, limit)
    
    def start_monitoring(self, interval: int = 30):
        """
        Inicia monitoramento automático das instâncias
        
        Args:
            interval: Intervalo em segundos para verificar status
        """
        if self._monitoring:
            return
        
        self._monitoring = True
        
        def monitor():
            while self._monitoring:
                try:
                    for instance_id, instance_info in self.instances.items():
                        handler = instance_info['handler']
                        is_ready = handler.is_ready()
                        
                        # Atualiza status no banco
                        status = 'connected' if is_ready else 'disconnected'
                        self.db.update_instance_status(instance_id, status)
                    
                    time.sleep(interval)
                except Exception as e:
                    print(f"[!] Erro no monitoramento: {e}")
                    time.sleep(interval)
        
        self._monitor_thread = threading.Thread(target=monitor, daemon=True)
        self._monitor_thread.start()
        print("[✓] Monitoramento de instâncias iniciado")
    
    def stop_monitoring(self):
        """Para monitoramento"""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2)
        print("[*] Monitoramento parado")
    
    def _get_instance_id_by_account(self, account_id: str) -> Optional[str]:
        """Retorna ID da instância pelo account_id"""
        instance_data = self.db.get_instance_by_account(account_id)
        return instance_data['id'] if instance_data else None
    
    def create_instance_for_account(self, account_id: str, instance_name: str, port: int) -> Dict:
        """
        Cria nova instância para uma conta
        
        Args:
            account_id: ID da conta
            instance_name: Nome da instância
            port: Porta do servidor Node.js
            
        Returns:
            Dados da instância criada
        """
        instance_data = {
            'account_id': account_id,
            'instance_name': instance_name,
            'port': port,
            'status': 'disconnected'
        }
        
        instance = self.db.create_instance(instance_data)
        
        # Cria handler
        handler = WhatsAppWebJSHandler(
            instance_name=instance_name,
            port=port
        )
        
        self.instances[instance['id']] = {
            'handler': handler,
            'data': instance
        }
        
        return instance

