"""
Handler de Inteligência Artificial
Suporta OpenAI e Anthropic
"""
import os
import json
import logging
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)


class AIHandler:
    """Handler simples para integração com IA"""
    
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "openai")  # openai ou anthropic
        self.api_key = os.getenv("AI_API_KEY", "")
        self.model = os.getenv("AI_MODEL", "gpt-4o-mini")
        self.system_prompt = os.getenv("AI_SYSTEM_PROMPT", "Você é um assistente útil e amigável.")
        self.conversation_history: Dict[str, List[Dict]] = {}  # phone -> messages
    
    def set_config(self, provider: str, api_key: str, model: str, system_prompt: str):
        """Configura a IA"""
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.system_prompt = system_prompt
    
    def get_response(self, phone: str, message: str, tenant_id: Optional[int] = None, 
                    instance_id: Optional[int] = None) -> str:
        """
        Obtém resposta da IA para uma mensagem
        
        Args:
            phone: Número do telefone (para manter contexto)
            message: Mensagem recebida
            tenant_id: ID do tenant (opcional, para buscar agente)
            instance_id: ID da instance (opcional, para buscar agente específico)
            
        Returns:
            Resposta da IA
        """
        # Busca agente configurado (se tenant_id/instance_id fornecidos)
        agent_config = None
        if instance_id or tenant_id:
            agent_config = self._get_agent_config(tenant_id, instance_id)
        
        # Usa configuração do agente ou padrão
        provider = agent_config.get('provider') if agent_config else self.provider
        api_key = agent_config.get('api_key') if agent_config else self.api_key
        model = agent_config.get('model') if agent_config else self.model
        system_prompt = agent_config.get('system_prompt') if agent_config else self.system_prompt
        temperature = agent_config.get('temperature', 0.7) if agent_config else 0.7
        max_tokens = agent_config.get('max_tokens', 500) if agent_config else 500  # Reduzido para respostas mais rápidas
        
        if not api_key:
            return "⚠️ IA não configurada. Configure sua API Key no dashboard."
        
        try:
            # Mantém histórico da conversa (usando chave única por phone + instance)
            history_key = f"{phone}_{instance_id or 'default'}"
            if history_key not in self.conversation_history:
                self.conversation_history[history_key] = [
                    {"role": "system", "content": system_prompt}
                ]
            
            # Adiciona mensagem do usuário
            self.conversation_history[history_key].append({
                "role": "user",
                "content": message
            })
            
            # Limita histórico (últimas 10 mensagens + system prompt)
            if len(self.conversation_history[history_key]) > 11:
                self.conversation_history[history_key] = (
                    [self.conversation_history[history_key][0]] +  # system prompt
                    self.conversation_history[history_key][-10:]  # últimas 10 mensagens
                )
            
            # Chama IA
            if provider == "openai":
                response = self._call_openai(history_key, api_key, model, temperature, max_tokens)
            elif provider == "anthropic":
                response = self._call_anthropic(history_key, api_key, model, system_prompt, max_tokens)
            else:
                return "⚠️ Provider de IA não suportado. Use 'openai' ou 'anthropic'."
            
            # Adiciona resposta ao histórico
            if history_key in self.conversation_history:
                self.conversation_history[history_key].append({
                    "role": "assistant",
                    "content": response
                })
            
            return response
            
        except Exception as e:
            return f"⚠️ Erro ao processar com IA: {str(e)}"
    
    def _get_agent_config(self, tenant_id: Optional[int] = None, instance_id: Optional[int] = None) -> Optional[Dict]:
        """
        Busca configuração do agente (da instance ou padrão do tenant)
        
        Args:
            tenant_id: ID do tenant
            instance_id: ID da instance (opcional)
        
        Returns:
            Dict com configuração do agente ou None
        """
        try:
            from src.database.db import SessionLocal
            from src.models.agent import Agent
            from src.models.instance import Instance
            
            db = SessionLocal()
            try:
                agent = None
                
                # Se instance_id fornecido, busca agente da instance
                if instance_id:
                    instance = db.query(Instance).filter(Instance.id == instance_id).first()
                    if instance and instance.agent_id:
                        agent = db.query(Agent).filter(
                            Agent.id == instance.agent_id,
                            Agent.is_active == True
                        ).first()
                    
                    # Se não encontrou, busca agente padrão do tenant
                    if not agent and instance:
                        agent = db.query(Agent).filter(
                            Agent.tenant_id == instance.tenant_id,
                            Agent.instance_id == None,
                            Agent.is_default == True,
                            Agent.is_active == True
                        ).first()
                
                # Se apenas tenant_id fornecido, busca agente padrão
                elif tenant_id:
                    agent = db.query(Agent).filter(
                        Agent.tenant_id == tenant_id,
                        Agent.instance_id == None,
                        Agent.is_default == True,
                        Agent.is_active == True
                    ).first()
                
                if agent:
                    # Busca API key do tenant ou usa padrão
                    api_key = self.api_key  # Por enquanto usa a configurada globalmente
                    # TODO: Adicionar campo api_key no Agent ou buscar do tenant
                    
                    return {
                        'provider': agent.provider,
                        'api_key': api_key,
                        'model': agent.model,
                        'system_prompt': agent.system_prompt,
                        'temperature': agent.temperature,
                        'max_tokens': agent.max_tokens,
                        'behavior_config': agent.behavior_config or {}
                    }
                
                return None
                
            finally:
                db.close()
                
        except Exception as e:
            logger.warning(f"Erro ao buscar agente: {e}")
            return None
    
    def _call_openai(self, history_key: str, api_key: str, model: str, temperature: float, max_tokens: int) -> str:
        """Chama OpenAI API"""
        try:
            import openai
            
            client = openai.OpenAI(api_key=api_key, timeout=15.0)  # Timeout de 15 segundos
            
            response = client.chat.completions.create(
                model=model,
                messages=self.conversation_history[history_key],
                temperature=temperature,
                max_tokens=min(max_tokens, 500),  # Limita a 500 tokens para respostas mais rápidas
                stream=False
            )
            
            text = response.choices[0].message.content.strip()
            # Formata o texto para melhor legibilidade (preserva quebras de linha)
            return self._format_response(text)
            
        except ImportError:
            return "⚠️ Biblioteca 'openai' não instalada. Execute: pip install openai"
        except Exception as e:
            return f"⚠️ Erro ao chamar OpenAI: {str(e)}"
    
    def _call_anthropic(self, history_key: str, api_key: str, model: str, system_prompt: str, max_tokens: int) -> str:
        """Chama Anthropic API"""
        try:
            from anthropic import Anthropic
            
            client = Anthropic(api_key=api_key, timeout=15.0)  # Timeout de 15 segundos
            
            # Converte formato OpenAI para Anthropic
            messages = []
            for msg in self.conversation_history[history_key]:
                if msg["role"] == "system":
                    continue  # Anthropic usa system diferente
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            response = client.messages.create(
                model=model,
                max_tokens=min(max_tokens, 500),  # Limita a 500 tokens para respostas mais rápidas
                system=system_prompt,
                messages=messages
            )
            
            text = response.content[0].text.strip()
            # Formata o texto para melhor legibilidade
            return self._format_response(text)
            
        except ImportError:
            return "⚠️ Biblioteca 'anthropic' não instalada. Execute: pip install anthropic"
        except Exception as e:
            return f"⚠️ Erro ao chamar Anthropic: {str(e)}"
    
    def _format_response(self, text: str) -> str:
        """
        Formata a resposta da IA para melhor legibilidade no WhatsApp
        - Preserva quebras de linha existentes
        - Adiciona quebras após pontos finais seguidos de espaço
        - Garante espaçamento adequado entre parágrafos
        """
        if not text:
            return text
        
        # Preserva quebras de linha existentes
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')  # Linha vazia para espaçamento
                continue
            
            # Se a linha é muito longa, tenta quebrar após pontos
            if len(line) > 80:
                # Quebra após pontos finais seguidos de espaço
                parts = line.split('. ')
                if len(parts) > 1:
                    formatted_parts = []
                    for i, part in enumerate(parts):
                        formatted_parts.append(part)
                        if i < len(parts) - 1:
                            formatted_parts.append('.')
                    formatted_lines.append(' '.join(formatted_parts))
                else:
                    formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        
        # Junta as linhas preservando quebras
        result = '\n'.join(formatted_lines)
        
        # Remove múltiplas linhas vazias consecutivas (máximo 2)
        while '\n\n\n' in result:
            result = result.replace('\n\n\n', '\n\n')
        
        return result.strip()
    
    def clear_history(self, phone: Optional[str] = None):
        """Limpa histórico de conversas"""
        if phone:
            if phone in self.conversation_history:
                del self.conversation_history[phone]
        else:
            self.conversation_history.clear()









