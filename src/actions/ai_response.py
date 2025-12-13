"""
Action: Resposta com IA
"""
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class AIResponseAction:
    """Ação para gerar e enviar resposta usando IA"""
    
    def execute(self, phone: str, conversation_id: Optional[int] = None,
               initial_message: Optional[str] = None, whatsapp_handler=None, **kwargs) -> Dict[str, Any]:
        """
        Gera resposta com IA e envia
        
        Args:
            phone: Número do telefone
            conversation_id: ID da conversa (opcional)
            initial_message: Mensagem que recebeu resposta
            whatsapp_handler: Handler do WhatsApp (opcional)
            **kwargs: Dados adicionais
        
        Returns:
            Dict com resultado
        """
        try:
            if not initial_message:
                return {
                    'success': False,
                    'error': 'Mensagem inicial não fornecida'
                }
            
            # Obtém handler da IA
            try:
                from src.ai_handler import AIHandler
                ai = AIHandler()
            except Exception as e:
                logger.error(f"Erro ao obter handler da IA: {e}")
                return {
                    'success': False,
                    'error': 'IA não disponível'
                }
            
            # Gera resposta com IA
            response = ai.get_response(phone, initial_message)
            
            if not response or response.startswith('⚠️'):
                return {
                    'success': False,
                    'error': response or 'IA não retornou resposta'
                }
            
            # Se não passou handler, tenta obter do contexto
            if not whatsapp_handler:
                try:
                    from web.app import whatsapp
                    whatsapp_handler = whatsapp
                except:
                    pass
            
            if not whatsapp_handler:
                return {
                    'success': False,
                    'error': 'Handler do WhatsApp não disponível'
                }
            
            # Envia resposta
            success = whatsapp_handler.send_message(phone, response)
            
            if success:
                logger.info(f"Resposta da IA enviada para {phone}")
                return {
                    'success': True,
                    'message': 'Resposta da IA enviada',
                    'response': response,
                    'phone': phone
                }
            else:
                return {
                    'success': False,
                    'error': 'Falha ao enviar resposta da IA'
                }
                
        except Exception as e:
            logger.error(f"Erro ao processar resposta da IA: {e}")
            return {
                'success': False,
                'error': str(e)
            }
