"""
Bot Ylada - Versão Simplificada
Apenas o essencial para uso imediato
"""
import sys
import os
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from conversation import ConversationManager
from contacts_manager import ContactsManager
from whatsapp_simple import WhatsAppSimpleHandler


class LadaBotSimple:
    """Bot simplificado - apenas o essencial"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.conversation = ConversationManager(config_path)
        self.contacts = ContactsManager()
        self.whatsapp = WhatsAppSimpleHandler()  # Sempre modo simples (gratuito)
        print("[✓] Bot Ylada iniciado (modo simples)")
    
    def process_incoming_message(self, phone: str, message: str) -> str:
        """Processa mensagem e retorna resposta"""
        # Registra contato
        self.contacts.get_or_create_contact(phone)
        self.contacts.add_message_to_history(phone, message, "received")
        
        # Processa
        response, _ = self.conversation.process_message(phone, message)
        
        # Registra resposta
        if response:
            self.contacts.add_message_to_history(phone, response, "sent")
        
        return response
    
    def send_message(self, phone: str, message: str) -> bool:
        """Envia mensagem (simulado no modo simples)"""
        return self.whatsapp.send_message(phone, message)
    
    def handle_webhook(self, webhook_data: Dict) -> Optional[str]:
        """Processa webhook"""
        if "phone" in webhook_data and "message" in webhook_data:
            phone = webhook_data["phone"]
            message = webhook_data["message"]
            
            if not message:
                return None
            
            response = self.process_incoming_message(phone, message)
            self.send_message(phone, response)
            
            return response
        return None

