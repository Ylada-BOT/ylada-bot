"""
Models: Conversation e Message
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from src.database.db import Base


class ConversationStatus(enum.Enum):
    """Status da conversa"""
    OPEN = "open"
    CLOSED = "closed"
    ARCHIVED = "archived"


class MessageDirection(enum.Enum):
    """Direção da mensagem"""
    INBOUND = "inbound"  # Recebida
    OUTBOUND = "outbound"  # Enviada


class MessageType(enum.Enum):
    """Tipo de mensagem"""
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    LOCATION = "location"
    CONTACT = "contact"


class Conversation(Base):
    """Conversa com um contato"""
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    instance_id = Column(Integer, ForeignKey('instances.id'), nullable=False)
    
    # Contato
    phone = Column(String(20), nullable=False, index=True)
    contact_name = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_cpf = Column(String(20), nullable=True)
    
    # Status
    status = Column(Enum(ConversationStatus), default=ConversationStatus.OPEN, nullable=False)
    
    # Estatísticas
    message_count = Column(Integer, default=0, nullable=False)
    unread_count = Column(Integer, default=0, nullable=False)
    last_message_at = Column(DateTime, nullable=True)
    
    # Atribuição e organização
    assigned_to = Column(Integer, ForeignKey('users.id'), nullable=True)
    tags = Column(JSON, default=list, nullable=True)  # Array de tags
    
    # Automação
    automation_enabled = Column(Boolean, default=True, nullable=False)
    
    # Metadados adicionais (usando extra_metadata para evitar conflito com palavra reservada)
    extra_metadata = Column(JSON, default=dict, nullable=True)
    
    # Lead
    is_lead = Column(Boolean, default=False, nullable=False)
    lead_id = Column(Integer, ForeignKey('leads.id'), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    tenant = relationship("Tenant", back_populates="conversations")
    instance = relationship("Instance", back_populates="conversations")
    # Conversation pertence a um Lead (many-to-one)
    lead = relationship("Lead", back_populates="conversation", foreign_keys=[lead_id])
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    assigned_user = relationship("User", foreign_keys=[assigned_to])
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, phone={self.phone}, status={self.status.value})>"


class Message(Base):
    """Mensagem de uma conversa"""
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    flow_id = Column(Integer, ForeignKey('flows.id'), nullable=True)
    
    # Conteúdo
    direction = Column(Enum(MessageDirection), nullable=False)
    type = Column(Enum(MessageType), default=MessageType.TEXT, nullable=False)
    content = Column(Text, nullable=True)
    media_url = Column(String(500), nullable=True)
    
    # Metadados
    whatsapp_id = Column(String(255), nullable=True, index=True)  # ID no WhatsApp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # IA
    is_ai_generated = Column(Boolean, default=False, nullable=False)
    ai_provider = Column(String(50), nullable=True)
    
    # Processamento
    processed = Column(Boolean, default=False, nullable=False)
    flow_executed = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relacionamentos
    conversation = relationship("Conversation", back_populates="messages")
    flow = relationship("Flow", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, direction={self.direction.value}, type={self.type.value})>"
