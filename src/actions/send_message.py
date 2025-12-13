"""
Action: Enviar Mensagem
"""
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class SendMessageAction:
    """Ação para enviar mensagem via WhatsApp"""
    
    def execute(self, phone: str, message: str, whatsapp_handler=None, **kwargs) -> Dict[str, Any]:
        """
        Envia uma mensagem
        
        Args:
            phone: Número do telefone
            message: Mensagem a enviar
            whatsapp_handler: Handler do WhatsApp (opcional)
            **kwargs: Dados adicionais
        
        Returns:
            Dict com resultado
        """
        try:
            if not message:
                return {
                    'success': False,
                    'error': 'Mensagem vazia'
                }
            
            # Se não passou handler, tenta obter do contexto
            if not whatsapp_handler:
                # Tenta importar o handler global (será configurado depois)
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
            
            # Envia mensagem
            success = whatsapp_handler.send_message(phone, message)
            
            if success:
                logger.info(f"Mensagem enviada para {phone}")
                return {
                    'success': True,
                    'message': 'Mensagem enviada com sucesso',
                    'phone': phone
                }
            else:
                return {
                    'success': False,
                    'error': 'Falha ao enviar mensagem'
                }
                
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            return {
                'success': False,
                'error': str(e)
            }
