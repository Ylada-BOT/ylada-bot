"""
Sistema de Fluxos de Conversação Avançado
Gerencia múltiplos fluxos, contexto e respostas inteligentes
"""
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import yaml
import os
import re


class ConversationFlows:
    """Gerencia fluxos de conversação configuráveis"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = self._load_config(config_path)
        self.flows_config = self.config.get("conversation_flows", {})
        self.keywords_config = self.config.get("keywords", {})
    
    def _load_config(self, path: str) -> Dict:
        """Carrega configuração"""
        if not os.path.exists(path):
            example_path = path.replace(".yaml", ".example.yaml")
            if os.path.exists(example_path):
                path = example_path
            else:
                return {}
        
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    
    def find_matching_flow(self, message: str, context: Dict) -> Optional[Dict]:
        """
        Encontra fluxo que corresponde à mensagem
        
        Args:
            message: Mensagem recebida
            context: Contexto da conversa
        
        Returns:
            Dict com informações do fluxo ou None
        """
        message_lower = message.lower().strip()
        current_flow = context.get("current_flow")
        
        # Se está em um fluxo, verifica se deve continuar ou sair
        if current_flow:
            flow_config = self.flows_config.get(current_flow, {})
            exit_keywords = flow_config.get("exit_keywords", [])
            
            # Verifica palavras de saída
            if any(kw in message_lower for kw in exit_keywords):
                return {
                    "flow": None,
                    "action": "exit_flow",
                    "response": flow_config.get("exit_message", "Ok, como posso ajudar?")
                }
        
        # Procura fluxo que corresponde
        for flow_name, flow_config in self.flows_config.items():
            trigger_keywords = flow_config.get("trigger_keywords", [])
            
            # Verifica palavras-chave de trigger
            if any(kw in message_lower for kw in trigger_keywords):
                return {
                    "flow": flow_name,
                    "action": "start_flow",
                    "response": flow_config.get("welcome_message", ""),
                    "steps": flow_config.get("steps", [])
                }
        
        # Verifica palavras-chave simples
        for keyword, response in self.keywords_config.items():
            if keyword in message_lower:
                return {
                    "flow": None,
                    "action": "keyword_response",
                    "response": response
                }
        
        return None
    
    def process_flow_step(self, flow_name: str, step_index: int, message: str, context: Dict) -> Tuple[str, Optional[int]]:
        """
        Processa um passo do fluxo
        
        Args:
            flow_name: Nome do fluxo
            step_index: Índice do passo atual
            message: Mensagem recebida
            context: Contexto da conversa
        
        Returns:
            Tuple (response, next_step_index)
        """
        flow_config = self.flows_config.get(flow_name, {})
        steps = flow_config.get("steps", [])
        
        if step_index >= len(steps):
            # Fluxo terminado
            return flow_config.get("end_message", "Obrigado!"), None
        
        current_step = steps[step_index]
        step_type = current_step.get("type", "message")
        
        if step_type == "message":
            # Apenas envia mensagem e avança
            return current_step.get("message", ""), step_index + 1
        
        elif step_type == "question":
            # Faz pergunta e espera resposta
            question = current_step.get("question", "")
            expected_responses = current_step.get("expected_responses", [])
            
            # Verifica se a resposta corresponde ao esperado
            message_lower = message.lower()
            for expected in expected_responses:
                if expected.get("keyword") in message_lower:
                    # Salva resposta no contexto
                    context["flow_data"] = context.get("flow_data", {})
                    context["flow_data"][current_step.get("save_as", "answer")] = message
                    
                    next_step = expected.get("next_step", step_index + 1)
                    response = expected.get("response", "")
                    return response, next_step
            
            # Resposta não esperada
            return current_step.get("error_message", "Desculpe, não entendi. Pode repetir?"), step_index
        
        elif step_type == "conditional":
            # Lógica condicional
            condition = current_step.get("condition", {})
            condition_field = condition.get("field")
            condition_value = condition.get("value")
            
            flow_data = context.get("flow_data", {})
            if flow_data.get(condition_field) == condition_value:
                return current_step.get("if_true", ""), current_step.get("if_true_step", step_index + 1)
            else:
                return current_step.get("if_false", ""), current_step.get("if_false_step", step_index + 1)
        
        # Tipo desconhecido, avança
        return "", step_index + 1
    
    def extract_entities(self, message: str) -> Dict[str, Any]:
        """
        Extrai entidades da mensagem (números, emails, etc.)
        
        Args:
            message: Mensagem recebida
        
        Returns:
            Dict com entidades extraídas
        """
        entities = {
            "phone_numbers": [],
            "emails": [],
            "numbers": []
        }
        
        # Extrai números de telefone
        phone_pattern = r'(\+?\d{1,3}?\s?\(?\d{2}\)?\s?\d{4,5}-?\d{4})'
        entities["phone_numbers"] = re.findall(phone_pattern, message)
        
        # Extrai emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        entities["emails"] = re.findall(email_pattern, message)
        
        # Extrai números
        number_pattern = r'\b\d+\b'
        entities["numbers"] = re.findall(number_pattern, message)
        
        return entities

