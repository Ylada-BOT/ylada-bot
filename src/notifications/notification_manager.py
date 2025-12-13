"""
Notification Manager
Gerencia notificações no banco de dados
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
import logging

from src.models.notification import Notification, NotificationType, NotificationStatus
from src.database.db import SessionLocal

logger = logging.getLogger(__name__)


class NotificationManager:
    """Gerencia notificações"""
    
    def __init__(self, db: Optional[Session] = None):
        """
        Inicializa o manager
        
        Args:
            db: Sessão do banco (opcional, cria nova se não fornecido)
        """
        self.db = db
    
    def _get_db(self) -> Session:
        """Obtém sessão do banco"""
        if self.db:
            return self.db
        return SessionLocal()
    
    def create_notification(
        self,
        tenant_id: int,
        notification_type: NotificationType,
        message: str,
        sent_to: str,
        title: Optional[str] = None,
        sent_to_name: Optional[str] = None,
        related_lead_id: Optional[int] = None,
        related_conversation_id: Optional[int] = None,
        related_flow_id: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Notification:
        """
        Cria uma nova notificação
        
        Args:
            tenant_id: ID do tenant
            notification_type: Tipo da notificação
            message: Mensagem a enviar
            sent_to: Número WhatsApp destino (formato: 5511999999999)
            title: Título opcional
            sent_to_name: Nome do destinatário
            related_lead_id: ID do lead relacionado (opcional)
            related_conversation_id: ID da conversa relacionada (opcional)
            related_flow_id: ID do fluxo relacionado (opcional)
            metadata: Dados adicionais (JSON)
        
        Returns:
            Notification criada
        """
        db = self._get_db()
        try:
            notification = Notification(
                tenant_id=tenant_id,
                type=notification_type,
                title=title,
                message=message,
                sent_to=sent_to,
                sent_to_name=sent_to_name,
                status=NotificationStatus.PENDING,
                related_lead_id=related_lead_id,
                related_conversation_id=related_conversation_id,
                related_flow_id=related_flow_id,
                metadata=metadata or {}
            )
            
            db.add(notification)
            db.commit()
            db.refresh(notification)
            
            logger.info(f"Notificação {notification.id} criada para {sent_to}")
            return notification
            
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao criar notificação: {e}")
            raise
        finally:
            if not self.db:
                db.close()
    
    def mark_as_sent(self, notification_id: int) -> bool:
        """
        Marca notificação como enviada
        
        Args:
            notification_id: ID da notificação
        
        Returns:
            True se atualizado
        """
        db = self._get_db()
        try:
            notification = db.query(Notification).filter(Notification.id == notification_id).first()
            if not notification:
                return False
            
            notification.status = NotificationStatus.SENT
            notification.sent_at = datetime.utcnow()
            
            db.commit()
            logger.info(f"Notificação {notification_id} marcada como enviada")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao marcar notificação como enviada: {e}")
            return False
        finally:
            if not self.db:
                db.close()
    
    def mark_as_failed(self, notification_id: int, error_message: str) -> bool:
        """
        Marca notificação como falhada
        
        Args:
            notification_id: ID da notificação
            error_message: Mensagem de erro
        
        Returns:
            True se atualizado
        """
        db = self._get_db()
        try:
            notification = db.query(Notification).filter(Notification.id == notification_id).first()
            if not notification:
                return False
            
            notification.status = NotificationStatus.FAILED
            notification.error_message = error_message
            
            db.commit()
            logger.info(f"Notificação {notification_id} marcada como falhada: {error_message}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao marcar notificação como falhada: {e}")
            return False
        finally:
            if not self.db:
                db.close()
    
    def get_notifications(
        self,
        tenant_id: Optional[int] = None,
        notification_type: Optional[NotificationType] = None,
        status: Optional[NotificationStatus] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Notification]:
        """
        Busca notificações
        
        Args:
            tenant_id: Filtrar por tenant (opcional)
            notification_type: Filtrar por tipo (opcional)
            status: Filtrar por status (opcional)
            limit: Limite de resultados
            offset: Offset para paginação
        
        Returns:
            Lista de notificações
        """
        db = self._get_db()
        try:
            query = db.query(Notification)
            
            if tenant_id:
                query = query.filter(Notification.tenant_id == tenant_id)
            
            if notification_type:
                query = query.filter(Notification.type == notification_type)
            
            if status:
                query = query.filter(Notification.status == status)
            
            query = query.order_by(desc(Notification.created_at))
            query = query.limit(limit).offset(offset)
            
            return query.all()
            
        except Exception as e:
            logger.error(f"Erro ao buscar notificações: {e}")
            return []
        finally:
            if not self.db:
                db.close()
    
    def get_pending_notifications(self, tenant_id: Optional[int] = None) -> List[Notification]:
        """
        Busca notificações pendentes
        
        Args:
            tenant_id: Filtrar por tenant (opcional)
        
        Returns:
            Lista de notificações pendentes
        """
        return self.get_notifications(
            tenant_id=tenant_id,
            status=NotificationStatus.PENDING
        )
    
    def get_notification(self, notification_id: int) -> Optional[Notification]:
        """
        Busca uma notificação por ID
        
        Args:
            notification_id: ID da notificação
        
        Returns:
            Notification ou None
        """
        db = self._get_db()
        try:
            return db.query(Notification).filter(Notification.id == notification_id).first()
        except Exception as e:
            logger.error(f"Erro ao buscar notificação {notification_id}: {e}")
            return None
        finally:
            if not self.db:
                db.close()
    
    def delete_notification(self, notification_id: int) -> bool:
        """
        Deleta uma notificação
        
        Args:
            notification_id: ID da notificação
        
        Returns:
            True se deletado
        """
        db = self._get_db()
        try:
            notification = db.query(Notification).filter(Notification.id == notification_id).first()
            if not notification:
                return False
            
            db.delete(notification)
            db.commit()
            logger.info(f"Notificação {notification_id} deletada")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao deletar notificação {notification_id}: {e}")
            return False
        finally:
            if not self.db:
                db.close()
