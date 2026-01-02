"""
Model: Flow (Fluxo de automação)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from src.database.db import Base


class FlowStatus(enum.Enum):
    """Status do fluxo"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DRAFT = "draft"


class Flow(Base):
    """Fluxo de automação"""
    __tablename__ = 'flows'
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    instance_id = Column(Integer, ForeignKey('instances.id'), nullable=True, index=True)  # NULL = compartilhado
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Dados do fluxo (JSON - estrutura do construtor visual)
    flow_data = Column(JSON, nullable=False, default=dict)
    
    # Configurações
    status = Column(Enum(FlowStatus), default=FlowStatus.DRAFT, nullable=False)
    trigger_keywords = Column(JSON, default=list, nullable=True)  # Palavras-chave que ativam
    trigger_conditions = Column(JSON, default=dict, nullable=True)  # Condições de ativação
    
    # Estatísticas
    times_executed = Column(Integer, default=0, nullable=False)
    last_executed_at = Column(DateTime, nullable=True)
    
    # Template
    is_template = Column(Boolean, default=False, nullable=False)
    template_category = Column(String(100), nullable=True)  # vendas, suporte, captacao
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    tenant = relationship("Tenant", back_populates="flows")
    messages = relationship("Message", back_populates="flow")
    
    def __repr__(self):
        return f"<Flow(id={self.id}, name={self.name}, status={self.status.value})>"
