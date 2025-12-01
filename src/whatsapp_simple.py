"""
Versão SIMPLES e GRATUITA - Funciona apenas na web (sem WhatsApp)
Para testes e desenvolvimento sem precisar de WhatsApp
"""
from typing import Dict, Optional
import json
import os
import time


class WhatsAppSimpleHandler:
    """
    Handler SIMPLES que funciona apenas na web
    
    Não precisa de WhatsApp, Z-API, ou nada!
    Perfeito para desenvolver e testar o bot.
    
    As mensagens são "simuladas" - você pode ver no dashboard web.
    """
    
    def __init__(self):
        self.messages_log = []
        self.messages_file = "data/messages_log.json"
        os.makedirs("data", exist_ok=True)
    
    def send_message(self, phone: str, message: str) -> bool:
        """
        Simula envio de mensagem (apenas loga)
        
        Args:
            phone: Número do destinatário
            message: Mensagem a ser enviada
        
        Returns:
            Sempre True (simulado)
        """
        log_entry = {
            "phone": phone,
            "message": message,
            "timestamp": time.time(),
            "status": "sent"
        }
        
        self.messages_log.append(log_entry)
        self._save_log()
        
        print(f"[SIMULADO] Mensagem para {phone}: {message}")
        return True
    
    def _save_log(self):
        """Salva log de mensagens"""
        try:
            with open(self.messages_file, "w", encoding="utf-8") as f:
                json.dump(self.messages_log, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[!] Erro ao salvar log: {e}")
    
    def get_messages_log(self) -> list:
        """Retorna log de mensagens enviadas"""
        return self.messages_log
    
    def format_phone(self, phone: str) -> str:
        """Formata número"""
        cleaned = ''.join(filter(str.isdigit, phone))
        if not cleaned.startswith(('1', '55')) and len(cleaned) in [10, 11]:
            cleaned = '55' + cleaned
        return cleaned
    
    def parse_webhook(self, data: Dict) -> Optional[Dict]:
        """Parse de webhook simulado"""
        if "phone" in data and "message" in data:
            return {
                "phone": self.format_phone(data["phone"]),
                "message": data.get("message", "").strip(),
                "name": data.get("name", ""),
                "timestamp": data.get("timestamp", "")
            }
        return None

