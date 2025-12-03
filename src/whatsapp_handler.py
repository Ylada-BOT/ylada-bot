"""
Integração com WhatsApp via Z-API
"""
import requests
from typing import Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class WhatsAppHandler:
    """Gerencia comunicação com WhatsApp via Z-API"""
    
    def __init__(self, instance_id: Optional[str] = None, token: Optional[str] = None, base_url: Optional[str] = None):
        self.instance_id = instance_id or os.getenv("ZAPI_INSTANCE_ID", "")
        self.token = token or os.getenv("ZAPI_TOKEN", "")
        self.base_url = base_url or os.getenv("ZAPI_BASE_URL", "https://api.z-api.io")
        
        if not self.instance_id or not self.token:
            raise ValueError("Z-API Instance ID e Token são obrigatórios")
    
    def send_message(self, phone: str, message: str) -> Dict:
        """
        Envia mensagem via Z-API
        
        Args:
            phone: Número do destinatário (formato: 5511999999999)
            message: Mensagem a ser enviada
        
        Returns:
            Resposta da API
        """
        url = f"{self.base_url}/instances/{self.instance_id}/token/{self.token}/send-text"
        
        payload = {
            "phone": phone,
            "message": message
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao enviar mensagem: {str(e)}")
    
    def send_image(self, phone: str, image_url: str, caption: Optional[str] = None) -> Dict:
        """Envia imagem via Z-API"""
        url = f"{self.base_url}/instances/{self.instance_id}/token/{self.token}/send-image"
        
        payload = {
            "phone": phone,
            "image": image_url,
        }
        if caption:
            payload["caption"] = caption
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao enviar imagem: {str(e)}")
    
    def send_document(self, phone: str, document_url: str, filename: str) -> Dict:
        """Envia documento via Z-API"""
        url = f"{self.base_url}/instances/{self.instance_id}/token/{self.token}/send-document"
        
        payload = {
            "phone": phone,
            "document": document_url,
            "fileName": filename
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao enviar documento: {str(e)}")
    
    def format_phone(self, phone: str) -> str:
        """
        Formata número de telefone para o padrão Z-API
        Remove caracteres especiais e garante formato internacional
        """
        # Remove caracteres não numéricos
        cleaned = ''.join(filter(str.isdigit, phone))
        
        # Se não começar com código do país, assume Brasil (55)
        if not cleaned.startswith(('1', '55')):
            # Se tiver 10 ou 11 dígitos, assume Brasil
            if len(cleaned) in [10, 11]:
                cleaned = '55' + cleaned
        
        return cleaned
    
    def parse_webhook(self, data: Dict) -> Optional[Dict]:
        """
        Parse do webhook do Z-API
        
        Returns:
            Dict com phone e message, ou None se não for mensagem válida
        """
        # Estrutura típica do webhook Z-API
        if "phone" in data and "message" in data:
            return {
                "phone": self.format_phone(data["phone"]),
                "message": data.get("message", "").strip(),
                "name": data.get("name", ""),
                "timestamp": data.get("timestamp", "")
            }
        
        # Outros formatos possíveis
        if "data" in data:
            msg_data = data["data"]
            if "phone" in msg_data and "message" in msg_data:
                return {
                    "phone": self.format_phone(msg_data["phone"]),
                    "message": msg_data.get("message", "").strip(),
                    "name": msg_data.get("name", ""),
                    "timestamp": msg_data.get("timestamp", "")
                }
        
        return None

