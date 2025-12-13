"""
Lead Capture
Detecta e captura leads automaticamente
"""
from typing import Optional, Dict, Any
import logging

from src.leads.lead_manager import LeadManager
from src.leads.lead_scoring import LeadScoring
from src.models.lead import LeadStatus
from src.notifications.notification_sender import NotificationSender

logger = logging.getLogger(__name__)


class LeadCapture:
    """Captura leads automaticamente"""
    
    def __init__(
        self,
        lead_manager: Optional[LeadManager] = None,
        lead_scoring: Optional[LeadScoring] = None,
        notification_sender: Optional[NotificationSender] = None
    ):
        """
        Inicializa o capturador
        
        Args:
            lead_manager: Manager de leads (opcional)
            lead_scoring: Calculador de score (opcional)
            notification_sender: Sender de notificações (opcional)
        """
        self.lead_manager = lead_manager or LeadManager()
        self.lead_scoring = lead_scoring or LeadScoring()
        self.notification_sender = notification_sender
    
    def capture_from_message(
        self,
        tenant_id: int,
        phone: str,
        message: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        source: str = 'flow',
        source_details: Optional[Dict[str, Any]] = None,
        conversation_id: Optional[int] = None,
        notify_to: Optional[str] = None,
        notify_to_name: Optional[str] = None
    ) -> Optional[Any]:
        """
        Captura lead a partir de uma mensagem
        
        Args:
            tenant_id: ID do tenant
            phone: Número do telefone
            message: Mensagem recebida
            name: Nome do lead (opcional, tenta extrair se não fornecido)
            email: Email do lead (opcional, tenta extrair se não fornecido)
            source: Origem do lead
            source_details: Detalhes da origem
            conversation_id: ID da conversa
            notify_to: Número para enviar notificação (opcional)
            notify_to_name: Nome do destinatário da notificação
        
        Returns:
            Lead capturado ou None
        """
        try:
            # Tenta extrair dados se não fornecidos
            if not name:
                name = self.lead_scoring.extract_name(message)
            
            if not email:
                email = self.lead_scoring.extract_email(message)
            
            # Verifica se já existe lead
            existing_lead = self.lead_manager.get_lead_by_phone(tenant_id, phone)
            
            # Calcula score
            score = self.lead_scoring.calculate_score(
                message=message,
                has_name=bool(name),
                has_email=bool(email),
                message_count=existing_lead.metadata.get('message_count', 0) + 1 if existing_lead else 1,
                source=source
            )
            
            # Atualiza contador de mensagens no metadata
            metadata = source_details or {}
            if existing_lead:
                metadata['message_count'] = existing_lead.extra_data.get('message_count', 0) + 1
            else:
                metadata['message_count'] = 1
            
            # Cria ou atualiza lead
            lead = self.lead_manager.create_lead(
                tenant_id=tenant_id,
                phone=phone,
                name=name,
                email=email,
                source=source,
                source_details=source_details,
                score=score,
                status=LeadStatus.NEW if not existing_lead else existing_lead.status,
                conversation_id=conversation_id,
                metadata=metadata
            )
            
            # Se é um novo lead, envia notificação
            if not existing_lead and self.notification_sender and notify_to:
                try:
                    lead_name = name or phone
                    self.notification_sender.notify_lead_captured(
                        tenant_id=tenant_id,
                        lead_id=lead.id,
                        lead_name=lead_name,
                        lead_phone=phone,
                        sent_to=notify_to,
                        sent_to_name=notify_to_name
                    )
                    logger.info(f"Notificação de lead {lead.id} enviada para {notify_to}")
                except Exception as e:
                    logger.warning(f"Erro ao enviar notificação de lead: {e}")
            
            logger.info(f"Lead {lead.id} capturado/atualizado para {phone} (score: {score})")
            return lead
            
        except Exception as e:
            logger.error(f"Erro ao capturar lead: {e}")
            return None
    
    def should_capture(self, message: str) -> bool:
        """
        Verifica se deve capturar lead baseado na mensagem
        
        Args:
            message: Mensagem recebida
        
        Returns:
            True se deve capturar
        """
        message_lower = message.lower()
        
        # Sempre captura se tem palavras-chave de interesse
        has_interest = any(keyword in message_lower for keyword in self.lead_scoring.INTEREST_KEYWORDS)
        
        # Captura se tem email ou nome mencionado
        has_email = self.lead_scoring.extract_email(message) is not None
        has_name = self.lead_scoring.extract_name(message) is not None
        
        # Captura se tem pelo menos um indicador
        return has_interest or has_email or has_name
    
    def capture_from_flow(
        self,
        tenant_id: int,
        phone: str,
        message: str,
        flow_id: int,
        flow_name: str,
        conversation_id: Optional[int] = None,
        notify_to: Optional[str] = None,
        notify_to_name: Optional[str] = None
    ) -> Optional[Any]:
        """
        Captura lead quando um fluxo é executado
        
        Args:
            tenant_id: ID do tenant
            phone: Número do telefone
            message: Mensagem recebida
            flow_id: ID do fluxo
            flow_name: Nome do fluxo
            conversation_id: ID da conversa
            notify_to: Número para enviar notificação
            notify_to_name: Nome do destinatário
        
        Returns:
            Lead capturado ou None
        """
        return self.capture_from_message(
            tenant_id=tenant_id,
            phone=phone,
            message=message,
            source='flow',
            source_details={
                'flow_id': flow_id,
                'flow_name': flow_name
            },
            conversation_id=conversation_id,
            notify_to=notify_to,
            notify_to_name=notify_to_name
        )
