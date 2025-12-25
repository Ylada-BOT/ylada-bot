"""
Handler de Inteligência Artificial
Suporta OpenAI e Anthropic
"""
import os
import json
from typing import Dict, Optional, List


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
    
    def get_response(self, phone: str, message: str) -> str:
        """
        Obtém resposta da IA para uma mensagem
        
        Args:
            phone: Número do telefone (para manter contexto)
            message: Mensagem recebida
            
        Returns:
            Resposta da IA
        """
        if not self.api_key:
            return "⚠️ IA não configurada. Configure sua API Key no dashboard."
        
        try:
            # Mantém histórico da conversa
            if phone not in self.conversation_history:
                self.conversation_history[phone] = [
                    {"role": "system", "content": self.system_prompt}
                ]
            
            # Adiciona mensagem do usuário
            self.conversation_history[phone].append({
                "role": "user",
                "content": message
            })
            
            # Limita histórico (últimas 10 mensagens + system prompt)
            if len(self.conversation_history[phone]) > 11:
                self.conversation_history[phone] = (
                    [self.conversation_history[phone][0]] +  # system prompt
                    self.conversation_history[phone][-10:]  # últimas 10 mensagens
                )
            
            # Chama IA
            if self.provider == "openai":
                response = self._call_openai(phone)
            elif self.provider == "anthropic":
                response = self._call_anthropic(phone)
            else:
                return "⚠️ Provider de IA não suportado. Use 'openai' ou 'anthropic'."
            
            # Adiciona resposta ao histórico
            if phone in self.conversation_history:
                self.conversation_history[phone].append({
                    "role": "assistant",
                    "content": response
                })
            
            return response
            
        except Exception as e:
            return f"⚠️ Erro ao processar com IA: {str(e)}"
    
    def _call_openai(self, phone: str) -> str:
        """Chama OpenAI API"""
        try:
            import openai
            
            openai.api_key = self.api_key
            client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history[phone],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except ImportError:
            return "⚠️ Biblioteca 'openai' não instalada. Execute: pip install openai"
        except Exception as e:
            return f"⚠️ Erro ao chamar OpenAI: {str(e)}"
    
    def _call_anthropic(self, phone: str) -> str:
        """Chama Anthropic API"""
        try:
            from anthropic import Anthropic
            
            client = Anthropic(api_key=self.api_key)
            
            # Converte formato OpenAI para Anthropic
            messages = []
            for msg in self.conversation_history[phone]:
                if msg["role"] == "system":
                    continue  # Anthropic usa system diferente
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            response = client.messages.create(
                model=self.model,
                max_tokens=500,
                system=self.system_prompt,
                messages=messages
            )
            
            return response.content[0].text.strip()
            
        except ImportError:
            return "⚠️ Biblioteca 'anthropic' não instalada. Execute: pip install anthropic"
        except Exception as e:
            return f"⚠️ Erro ao chamar Anthropic: {str(e)}"
    
    def clear_history(self, phone: Optional[str] = None):
        """Limpa histórico de conversas"""
        if phone:
            if phone in self.conversation_history:
                del self.conversation_history[phone]
        else:
            self.conversation_history.clear()








