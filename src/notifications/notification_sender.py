"""
Notification Sender
Envia notificações via WhatsApp
"""
from typing import Optional
import logging

from src.notifications.notification_manager import NotificationManager
from src.models.notification import Notification, NotificationType

logger = logging.getLogger(__name__)


class NotificationSender:
    """Envia notificações via WhatsApp"""
    
    def __init__(self, whatsapp_handler, notification_manager: Optional[NotificationManager] = None):
        """
        Inicializa o sender
        
        Args:
            whatsapp_handler: Handler do WhatsApp (WhatsAppWebJSHandler)
            notification_manager: Manager de notificações (opcional)
        """
        self.whatsapp_handler = whatsapp_handler
        self.notification_manager = notification_manager or NotificationManager()
    
    def send_notification(self, notification: Notification) -> bool:
        """
        Envia uma notificação
        
        Args:
            notification: Notification a enviar
        
        Returns:
            True se enviado com sucesso
        """
        try:
            if not self.whatsapp_handler:
                logger.error("Handler do WhatsApp não disponível")
                self.notification_manager.mark_as_failed(
                    notification.id,
                    "Handler do WhatsApp não disponível"
                )
                return False
            
            if not self.whatsapp_handler.is_ready():
                logger.error("WhatsApp não está conectado")
                self.notification_manager.mark_as_failed(
                    notification.id,
                    "WhatsApp não está conectado"
                )
                return False
            
            # Formata mensagem
            message = self._format_message(notification)
            
            # Envia mensagem
            success = self.whatsapp_handler.send_message(
                notification.sent_to,
                message
            )
            
            if success:
                self.notification_manager.mark_as_sent(notification.id)
                logger.info(f"Notificação {notification.id} enviada para {notification.sent_to}")
                return True
            else:
                self.notification_manager.mark_as_failed(
                    notification.id,
                    "Falha ao enviar mensagem via WhatsApp"
                )
                return False
                
        except Exception as e:
            logger.error(f"Erro ao enviar notificação {notification.id}: {e}")
            self.notification_manager.mark_as_failed(
                notification.id,
                str(e)
            )
            return False
    
    def send_pending_notifications(self, tenant_id: Optional[int] = None) -> int:
        """
        Envia todas as notificações pendentes
        
        Args:
            tenant_id: Filtrar por tenant (opcional)
        
        Returns:
            Número de notificações enviadas
        """
        pending = self.notification_manager.get_pending_notifications(tenant_id=tenant_id)
        sent_count = 0
        
        for notification in pending:
            if self.send_notification(notification):
                sent_count += 1
        
        logger.info(f"{sent_count}/{len(pending)} notificações enviadas")
        return sent_count
    
    def _format_message(self, notification: Notification) -> str:
        """
        Formata mensagem da notificação
        
        Args:
            notification: Notification
        
        Returns:
            Mensagem formatada
        """
        # Se tem título, usa título + mensagem
        if notification.title:
            message = f"*{notification.title}*\n\n{notification.message}"
        else:
            message = notification.message
        
        # Adiciona informações contextuais baseado no tipo
        if notification.type == NotificationType.FLOW_TRIGGERED:
            if notification.related_flow_id:
                message += f"\n\n📋 Fluxo ID: {notification.related_flow_id}"
        
        elif notification.type == NotificationType.LEAD_CAPTURED:
            if notification.related_lead_id:
                message += f"\n\n🎯 Lead ID: {notification.related_lead_id}"
        
        elif notification.type == NotificationType.CONVERSION:
            if notification.related_conversation_id:
                message += f"\n\n💬 Conversa ID: {notification.related_conversation_id}"
        
        return message
    
    def notify_flow_triggered(
        self,
        tenant_id: int,
        flow_id: int,
        flow_name: str,
        phone: str,
        sent_to: str,
        sent_to_name: Optional[str] = None
    ) -> Optional[Notification]:
        """
        Cria e envia notificação quando um fluxo é executado
        
        Args:
            tenant_id: ID do tenant
            flow_id: ID do fluxo
            flow_name: Nome do fluxo
            phone: Número que disparou o fluxo
            sent_to: Número WhatsApp destino
            sent_to_name: Nome do destinatário
        
        Returns:
            Notification criada
        """
        notification = self.notification_manager.create_notification(
            tenant_id=tenant_id,
            notification_type=NotificationType.FLOW_TRIGGERED,
            title="🔄 Fluxo Executado",
            message=f"O fluxo *{flow_name}* foi executado para o número {phone}",
            sent_to=sent_to,
            sent_to_name=sent_to_name,
            related_flow_id=flow_id,
            metadata={
                'flow_name': flow_name,
                'triggered_by': phone
            }
        )
        
        # Tenta enviar imediatamente
        self.send_notification(notification)
        
        return notification
    
    def notify_lead_captured(
        self,
        tenant_id: int,
        lead_id: int,
        lead_name: str,
        lead_phone: str,
        sent_to: str,
        sent_to_name: Optional[str] = None
    ) -> Optional[Notification]:
        """
        Cria e envia notificação quando um lead é capturado
        
        Args:
            tenant_id: ID do tenant
            lead_id: ID do lead
            lead_name: Nome do lead
            lead_phone: Telefone do lead
            sent_to: Número WhatsApp destino
            sent_to_name: Nome do destinatário
        
        Returns:
            Notification criada
        """
        notification = self.notification_manager.create_notification(
            tenant_id=tenant_id,
            notification_type=NotificationType.LEAD_CAPTURED,
            title="🎯 Novo Lead Capturado",
            message=f"Novo lead capturado:\n\n*{lead_name}*\n{lead_phone}",
            sent_to=sent_to,
            sent_to_name=sent_to_name,
            related_lead_id=lead_id,
            metadata={
                'lead_name': lead_name,
                'lead_phone': lead_phone
            }
        )
        
        # Tenta enviar imediatamente
        self.send_notification(notification)
        
        return notification
    
    def notify_custom(
        self,
        tenant_id: int,
        message: str,
        sent_to: str,
        title: Optional[str] = None,
        sent_to_name: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> Optional[Notification]:
        """
        Cria e envia notificação customizada
        
        Args:
            tenant_id: ID do tenant
            message: Mensagem
            sent_to: Número WhatsApp destino
            title: Título (opcional)
            sent_to_name: Nome do destinatário
            metadata: Dados adicionais
        
        Returns:
            Notification criada
        """
        notification = self.notification_manager.create_notification(
            tenant_id=tenant_id,
            notification_type=NotificationType.CUSTOM,
            title=title,
            message=message,
            sent_to=sent_to,
            sent_to_name=sent_to_name,
            metadata=metadata or {}
        )
        
        # Tenta enviar imediatamente
        self.send_notification(notification)
        
        return notification
