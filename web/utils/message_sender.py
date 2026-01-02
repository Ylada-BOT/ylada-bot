"""
Helper para enviar mensagens via fila

Centraliza o envio de mensagens para usar sempre a fila.
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def send_message_via_queue(
    phone: str,
    message: str,
    tenant_id: Optional[int] = None,
    instance_id: Optional[int] = None,
    priority: int = 0,
    use_queue: bool = True
) -> dict:
    """
    Envia mensagem via fila (ou diretamente se fila não disponível)
    
    Args:
        phone: Número de telefone
        message: Mensagem a enviar
        tenant_id: ID do tenant (opcional)
        instance_id: ID da instância/bot (opcional)
        priority: Prioridade (maior = mais prioritário, padrão: 0)
        use_queue: Se True, usa fila; se False, envia diretamente
    
    Returns:
        Dict com resultado:
        {
            'success': bool,
            'message_id': str (se via fila),
            'message': str
        }
    """
    from web.utils.message_queue import get_message_queue
    
    # Tenta usar fila se disponível e solicitado
    if use_queue:
        queue = get_message_queue()
        if queue:
            try:
                message_id = queue.add_message(
                    phone=phone,
                    message=message,
                    tenant_id=tenant_id,
                    instance_id=instance_id,
                    priority=priority
                )
                logger.info(f"✅ Mensagem adicionada à fila: {message_id}")
                return {
                    'success': True,
                    'message_id': message_id,
                    'message': 'Mensagem adicionada à fila',
                    'via_queue': True
                }
            except Exception as e:
                logger.error(f"❌ Erro ao adicionar mensagem à fila: {e}")
                # Fallback para envio direto
                logger.info("🔄 Tentando envio direto como fallback...")
    
    # Fallback: envio direto (sem fila)
    try:
        from web.app import whatsapp
        
        if not whatsapp:
            return {
                'success': False,
                'error': 'WhatsApp não inicializado',
                'via_queue': False
            }
        
        if not whatsapp.is_ready():
            return {
                'success': False,
                'error': 'WhatsApp não está conectado',
                'via_queue': False
            }
        
        success = whatsapp.send_message(phone, message)
        
        if success:
            logger.info(f"✅ Mensagem enviada diretamente para {phone}")
            return {
                'success': True,
                'message': 'Mensagem enviada diretamente',
                'via_queue': False
            }
        else:
            return {
                'success': False,
                'error': 'Falha ao enviar mensagem',
                'via_queue': False
            }
            
    except Exception as e:
        logger.error(f"❌ Erro ao enviar mensagem diretamente: {e}")
        return {
            'success': False,
            'error': str(e),
            'via_queue': False
        }



