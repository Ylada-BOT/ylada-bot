"""
Sistema de gerenciamento de conversas do Bot Ylada
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import yaml
import os
from conversation_flows import ConversationFlows


class ConversationManager:
    """Gerencia o fluxo de conversação do bot"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = self._load_config(config_path)
        self.conversations: Dict[str, Dict] = {}  # phone -> conversation state
        self.flows = self.config.get("flows", {})
        self.bot_name = self.config.get("bot", {}).get("name", "Ylada")
        self.welcome_msg = self.config.get("bot", {}).get("welcome_message", "Olá! 👋")
        self.default_response = self.config.get("bot", {}).get("default_response", "Desculpe, não entendi.")
        
        # Sistema de fluxos avançado
        self.flows_manager = ConversationFlows(config_path)
    
    def _load_config(self, path: str) -> Dict:
        """Carrega configuração do arquivo YAML"""
        if not os.path.exists(path):
            # Tenta o exemplo
            example_path = path.replace(".yaml", ".example.yaml")
            if os.path.exists(example_path):
                path = example_path
            else:
                return {}
        
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    
    def get_conversation(self, phone: str) -> Dict:
        """Obtém ou cria uma conversa para um número"""
        if phone not in self.conversations:
            self.conversations[phone] = {
                "phone": phone,
                "state": "idle",
                "context": {},
                "created_at": datetime.now().isoformat(),
                "last_message_at": datetime.now().isoformat(),
                "message_count": 0
            }
        return self.conversations[phone]
    
    def update_conversation(self, phone: str, state: Optional[str] = None, context: Optional[Dict] = None):
        """Atualiza o estado da conversa"""
        conv = self.get_conversation(phone)
        if state:
            conv["state"] = state
        if context:
            conv["context"].update(context)
        conv["last_message_at"] = datetime.now().isoformat()
        conv["message_count"] += 1
    
    def process_message(self, phone: str, message: str) -> Tuple[str, str]:
        """
        Processa mensagem e retorna (response, new_state)
        """
        message_lower = message.lower().strip()
        conv = self.get_conversation(phone)
        current_state = conv["state"]
        context = conv.get("context", {})
        
        # Tenta usar sistema de fluxos avançado primeiro
        flow_match = self.flows_manager.find_matching_flow(message, context)
        
        if flow_match:
            action = flow_match.get("action")
            
            if action == "start_flow":
                # Inicia novo fluxo
                flow_name = flow_match.get("flow")
                context["current_flow"] = flow_name
                context["flow_step"] = 0
                context["flow_data"] = {}
                self.update_conversation(phone, state=f"flow:{flow_name}", context=context)
                return flow_match.get("response", ""), f"flow:{flow_name}"
            
            elif action == "exit_flow":
                # Sai do fluxo atual
                context.pop("current_flow", None)
                context.pop("flow_step", None)
                self.update_conversation(phone, state="idle", context=context)
                return flow_match.get("response", ""), "idle"
            
            elif action == "keyword_response":
                # Resposta simples por palavra-chave
                return flow_match.get("response", ""), current_state
        
        # Se está em um fluxo, processa passo do fluxo
        if current_state.startswith("flow:"):
            flow_name = current_state.replace("flow:", "")
            step_index = context.get("flow_step", 0)
            
            response, next_step = self.flows_manager.process_flow_step(
                flow_name, step_index, message, context
            )
            
            if next_step is None:
                # Fluxo terminou
                context.pop("current_flow", None)
                context.pop("flow_step", None)
                self.update_conversation(phone, state="idle", context=context)
            else:
                # Continua no fluxo
                context["flow_step"] = next_step
                self.update_conversation(phone, state=current_state, context=context)
            
            return response, current_state if next_step is not None else "idle"
        
        # Detectar intenções básicas (fallback)
        if self._matches_flow(message_lower, "greeting"):
            self.update_conversation(phone, state="greeting")
            return self.welcome_msg, "greeting"
        
        if self._matches_flow(message_lower, "help"):
            help_text = self._get_help_message()
            self.update_conversation(phone, state="help")
            return help_text, "help"
        
        if self._matches_flow(message_lower, "services"):
            services_text = self._get_services_message()
            self.update_conversation(phone, state="services")
            return services_text, "services"
        
        # Estados específicos
        if current_state == "greeting":
            return "Como posso ajudar você hoje? Digite *ajuda* para ver opções.", "idle"
        
        if current_state == "services":
            return "Gostaria de mais informações sobre algum serviço específico?", "idle"
        
        # Resposta padrão
        return self.default_response, "idle"
    
    def _matches_flow(self, message: str, flow_name: str) -> bool:
        """Verifica se a mensagem corresponde a um fluxo"""
        flow_keywords = self.flows.get(flow_name, [])
        return any(keyword in message for keyword in flow_keywords)
    
    def _get_help_message(self) -> str:
        """Retorna mensagem de ajuda"""
        return f"""🤖 *Menu de Ajuda - {self.bot_name}*

📋 *Comandos disponíveis:*
• *Serviços* - Ver nossos serviços
• *Ajuda* - Ver este menu
• *Contato* - Falar com atendente

Digite o comando desejado! 😊"""
    
    def _get_services_message(self) -> str:
        """Retorna mensagem de serviços"""
        return f"""🛍️ *Nossos Serviços - {self.bot_name}*

Aqui você encontra:
• Serviço 1
• Serviço 2
• Serviço 3

Gostaria de mais informações sobre algum? Digite o número ou nome do serviço!"""
    
    def reset_conversation(self, phone: str):
        """Reseta a conversa de um número"""
        if phone in self.conversations:
            del self.conversations[phone]

