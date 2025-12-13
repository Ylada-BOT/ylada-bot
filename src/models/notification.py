"""
Model: Notification (Notificação)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from src.database.db import Base


class NotificationType(enum.Enum):
    """Tipo de notificação"""
    LEAD_CAPTURED = "lead_captured"
    CONVERSION = "conversion"
    MESSAGE_RECEIVED = "message_received"
    FLOW_TRIGGERED = "flow_triggered"
    SYSTEM_ALERT = "system_alert"
    PAYMENT = "payment"
    CUSTOM = "custom"


class NotificationStatus(enum.Enum):
    """Status da notificação"""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Notification(Base):
    """Notificação para outro WhatsApp"""
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    
    # Tipo e conteúdo
    type = Column(Enum(NotificationType), nullable=False)
    title = Column(String(255), nullable=True)
    message = Column(Text, nullable=False)
    
    # Destino
    sent_to = Column(String(20), nullable=False)  # Número WhatsApp destino
    sent_to_name = Column(String(255), nullable=True)
    
    # Status
    status = Column(Enum(NotificationStatus), default=NotificationStatus.PENDING, nullable=False)
    sent_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Dados adicionais (JSON)
    extra_data = Column('metadata', JSON, default=dict, nullable=True)  # Mapeado para 'metadata' no banco
    
    # Relacionamentos
    related_lead_id = Column(Integer, ForeignKey('leads.id'), nullable=True)
    related_conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=True)
    related_flow_id = Column(Integer, ForeignKey('flows.id'), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    tenant = relationship("Tenant", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification(id={self.id}, type={self.type.value}, status={self.status.value})>"
