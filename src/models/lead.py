"""
Model: Lead (Lead capturado)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from src.database.db import Base


class LeadStatus(enum.Enum):
    """Status do lead"""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    CONVERTED = "converted"
    LOST = "lost"


class Lead(Base):
    """Lead capturado"""
    __tablename__ = 'leads'
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    
    # Dados do lead
    phone = Column(String(20), nullable=False, index=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Origem
    source = Column(String(100), nullable=True)  # flow, manual, api, etc
    source_details = Column(JSON, default=dict, nullable=True)
    
    # Qualificação
    score = Column(Float, default=0.0, nullable=False)  # 0-100
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW, nullable=False)
    
    # Dados adicionais (JSON)
    extra_data = Column('metadata', JSON, default=dict, nullable=True)  # Mapeado para 'metadata' no banco
    tags = Column(JSON, default=list, nullable=True)
    
    # Datas
    first_contact_at = Column(DateTime, nullable=True)
    last_contact_at = Column(DateTime, nullable=True)
    converted_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    tenant = relationship("Tenant", back_populates="leads")
    # Lead pode ter uma Conversation (one-to-one)
    # Conversation tem lead_id (FK), então Lead tem one-to-one com Conversation
    conversation = relationship("Conversation", back_populates="lead", uselist=False)
    
    def __repr__(self):
        return f"<Lead(id={self.id}, phone={self.phone}, status={self.status.value}, score={self.score})>"
