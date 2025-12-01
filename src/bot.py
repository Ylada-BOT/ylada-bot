"""
Bot principal do Ylada - Integra conversação e WhatsApp
"""
import sys
import os
from typing import Dict, Optional

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from conversation import ConversationManager
from whatsapp_handler import WhatsAppHandler
from whatsapp_simple import WhatsAppSimpleHandler
from whatsapp_web_handler import WhatsAppWebHandler
from whatsapp_webjs_handler import WhatsAppWebJSHandler
from contacts_manager import ContactsManager


class LadaBot:
    """Bot principal do Ylada"""
    
    def __init__(self, config_path: str = "config/config.yaml", mode: str = "simple"):
        """
        Inicializa o bot
        
        Args:
            config_path: Caminho do arquivo de configuração
            mode: Modo de operação
                - "simple": Modo gratuito (simulado, apenas web)
                - "web": WhatsApp Web direto (gratuito, precisa conectar)
                - "zapi": Z-API (pago)
        """
        self.conversation = ConversationManager(config_path)
        self.contacts = ContactsManager()
        self.whatsapp = None
        self.mode = mode
        
        # Escolhe handler baseado no modo
        if mode == "simple":
            print("[*] Modo SIMPLES ativado (gratuito, apenas web)")
            self.whatsapp = WhatsAppSimpleHandler()
        
        elif mode == "web":
            print("[*] Modo WhatsApp Web ativado (gratuito)")
            try:
                self.whatsapp = WhatsAppWebHandler(use_playwright=True, headless=False)
                print("[*] Conecte ao WhatsApp Web quando o navegador abrir")
            except Exception as e:
                print(f"[!] Erro ao inicializar WhatsApp Web: {e}")
                print("[!] Instale: pip install playwright && playwright install chromium")
                print("[!] Usando modo SIMPLES como fallback")
                self.whatsapp = WhatsAppSimpleHandler()
                self.mode = "simple"
        
        elif mode == "webjs":
            print("[*] Modo WhatsApp Web.js ativado (gratuito, múltiplas instâncias)")
            try:
                self.whatsapp = WhatsAppWebJSHandler(instance_name="ylada_bot", port=3000)
                if self.whatsapp.start_server():
                    print("[*] Servidor iniciado! Escaneie o QR Code que aparecerá")
                    print("[*] Aguardando conexão...")
                    # Aguarda um pouco para conectar
                    import time
                    time.sleep(2)
                else:
                    print("[!] Erro ao iniciar servidor. Verifique se Node.js está instalado")
                    print("[!] Instale: https://nodejs.org")
                    print("[!] Usando modo SIMPLES como fallback")
                    self.whatsapp = WhatsAppSimpleHandler()
                    self.mode = "simple"
            except Exception as e:
                print(f"[!] Erro ao inicializar WhatsApp Web.js: {e}")
                print("[!] Instale Node.js: https://nodejs.org")
                print("[!] Depois: npm install whatsapp-web.js qrcode-terminal express")
                print("[!] Usando modo SIMPLES como fallback")
                self.whatsapp = WhatsAppSimpleHandler()
                self.mode = "simple"
        
        elif mode == "zapi":
            # Modo Z-API (pago)
            try:
                config = self.conversation.config
                zapi_config = config.get("zapi", {})
                if zapi_config.get("instance_id") and zapi_config.get("token"):
                    self.whatsapp = WhatsAppHandler(
                        instance_id=zapi_config["instance_id"],
                        token=zapi_config["token"],
                        base_url=zapi_config.get("base_url", "https://api.z-api.io")
                    )
                    print("[*] Modo Z-API ativado")
                else:
                    print("[!] Z-API não configurado. Usando modo SIMPLES")
                    self.whatsapp = WhatsAppSimpleHandler()
                    self.mode = "simple"
            except Exception as e:
                print(f"[!] Erro ao inicializar Z-API: {e}")
                print("[!] Usando modo SIMPLES como fallback")
                self.whatsapp = WhatsAppSimpleHandler()
                self.mode = "simple"
        
        else:
            print(f"[!] Modo '{mode}' desconhecido. Usando modo SIMPLES")
            self.whatsapp = WhatsAppSimpleHandler()
            self.mode = "simple"
    
    def process_incoming_message(self, phone: str, message: str) -> str:
        """
        Processa mensagem recebida e retorna resposta
        
        Args:
            phone: Número do remetente
            message: Mensagem recebida
        
        Returns:
            Resposta do bot
        """
        # Registra contato e mensagem
        self.contacts.get_or_create_contact(phone)
        self.contacts.add_message_to_history(phone, message, "received")
        
        # Processa mensagem
        response, new_state = self.conversation.process_message(phone, message)
        
        # Registra resposta enviada
        if response:
            self.contacts.add_message_to_history(phone, response, "sent")
        
        return response
    
    def send_message(self, phone: str, message: str) -> bool:
        """
        Envia mensagem via WhatsApp
        
        Args:
            phone: Número do destinatário
            message: Mensagem a ser enviada
        
        Returns:
            True se enviado com sucesso
        """
        if not self.whatsapp:
            print(f"[!] WhatsApp não configurado. Mensagem que seria enviada: {message}")
            return False
        
        try:
            formatted_phone = self.whatsapp.format_phone(phone)
            
            # Se for modo web, precisa estar conectado
            if self.mode == "web" and not self.whatsapp.is_connected:
                print("[!] WhatsApp Web não conectado. Conecte primeiro com bot.connect_whatsapp()")
                return False
            
            # Se for modo webjs, verifica se está pronto
            if self.mode == "webjs" and not self.whatsapp.is_ready():
                print("[!] WhatsApp Web.js não conectado. Escaneie o QR Code primeiro")
                return False
            
            result = self.whatsapp.send_message(formatted_phone, message)
            print(f"[✓] Mensagem enviada para {formatted_phone} (modo: {self.mode})")
            return True
        except Exception as e:
            print(f"[!] Erro ao enviar mensagem: {e}")
            return False
    
    def connect_whatsapp(self) -> bool:
        """
        Conecta ao WhatsApp Web (apenas modo "web")
        
        Returns:
            True se conectado
        """
        if self.mode == "web" and self.whatsapp:
            return self.whatsapp.connect()
        else:
            print("[!] Modo web não ativado")
            return False
    
    def handle_webhook(self, webhook_data: Dict) -> Optional[str]:
        """
        Processa webhook do Z-API
        
        Args:
            webhook_data: Dados do webhook
        
        Returns:
            Resposta do bot ou None
        """
        if not self.whatsapp:
            return None
        
        parsed = self.whatsapp.parse_webhook(webhook_data)
        if not parsed:
            return None
        
        phone = parsed["phone"]
        message = parsed["message"]
        
        # Ignora mensagens vazias
        if not message:
            return None
        
        # Processa mensagem (já registra no histórico)
        response = self.process_incoming_message(phone, message)
        
        # Envia resposta
        self.send_message(phone, response)
        
        return response

