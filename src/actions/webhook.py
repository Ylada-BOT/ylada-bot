"""
Action: Chamar Webhook Externo
"""
from typing import Dict, Any, Optional
import requests
import logging

logger = logging.getLogger(__name__)


class WebhookAction:
    """Ação para chamar webhook externo"""
    
    def execute(self, url: str, method: str = 'POST', data: Optional[Dict] = None,
               phone: str = '', **kwargs) -> Dict[str, Any]:
        """
        Chama um webhook externo
        
        Args:
            url: URL do webhook
            method: Método HTTP (GET, POST, etc)
            data: Dados a enviar
            phone: Número do telefone
            **kwargs: Dados adicionais
        
        Returns:
            Dict com resultado
        """
        try:
            if not url:
                return {
                    'success': False,
                    'error': 'URL do webhook não fornecida'
                }
            
            # Prepara dados
            payload = data or {}
            payload['phone'] = phone
            payload.update(kwargs)
            
            # Chama webhook
            if method.upper() == 'GET':
                response = requests.get(url, params=payload, timeout=10)
            else:
                response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code >= 200 and response.status_code < 300:
                logger.info(f"Webhook chamado com sucesso: {url}")
                return {
                    'success': True,
                    'message': 'Webhook chamado com sucesso',
                    'status_code': response.status_code,
                    'response': response.text[:500]  # Limita tamanho
                }
            else:
                return {
                    'success': False,
                    'error': f'Webhook retornou status {response.status_code}',
                    'status_code': response.status_code
                }
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao chamar webhook: {url}")
            return {
                'success': False,
                'error': 'Timeout ao chamar webhook'
            }
        except Exception as e:
            logger.error(f"Erro ao chamar webhook: {e}")
            return {
                'success': False,
                'error': str(e)
            }
