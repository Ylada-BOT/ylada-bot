"""
Model: Instance (Instância WhatsApp)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from src.database.db import Base


class InstanceStatus(enum.Enum):
    """Status da instância"""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"


class Instance(Base):
    """Instância WhatsApp de um tenant"""
    __tablename__ = 'instances'
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=True)
    status = Column(Enum(InstanceStatus), default=InstanceStatus.DISCONNECTED, nullable=False)
    
    # Dados da sessão (criptografado)
    session_data = Column(Text, nullable=True)
    session_dir = Column(String(500), nullable=True)
    
    # Configurações
    port = Column(Integer, default=5001, nullable=False)
    webhook_url = Column(String(500), nullable=True)
    
    # Estatísticas
    messages_sent = Column(Integer, default=0, nullable=False)
    messages_received = Column(Integer, default=0, nullable=False)
    last_message_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    tenant = relationship("Tenant", back_populates="instances")
    conversations = relationship("Conversation", back_populates="instance", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Instance(id={self.id}, name={self.name}, status={self.status.value})>"
