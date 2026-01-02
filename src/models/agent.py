"""
Model: Agent (Agente de IA)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.db import Base


class Agent(Base):
    """Agente de IA configurado"""
    __tablename__ = 'agents'
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    instance_id = Column(Integer, ForeignKey('instances.id'), nullable=True)  # NULL = agente padrão da org
    
    # Informações básicas
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Configuração de IA
    provider = Column(String(50), nullable=False, default='openai')  # openai, anthropic, etc
    model = Column(String(100), nullable=False, default='gpt-4o-mini')  # gpt-4o-mini, claude-3-haiku, etc
    system_prompt = Column(Text, nullable=False, default='Você é um assistente útil e amigável.')
    temperature = Column(Float, default=0.7, nullable=False)
    max_tokens = Column(Integer, default=1000, nullable=False)
    
    # Configurações extras (JSON)
    behavior_config = Column(JSON, default=dict, nullable=True)  # Configurações extras
    
    # Status
    is_default = Column(Boolean, default=False, nullable=False)  # Agente padrão da org/instance
    is_active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    tenant = relationship("Tenant", back_populates="agents")
    # instance_id é apenas para indicar se o agente é específico de uma instance
    # O relacionamento real é através de instances.agent_id
    
    def __repr__(self):
        return f"<Agent(id={self.id}, name={self.name}, provider={self.provider}, model={self.model})>"
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'instance_id': self.instance_id,
            'name': self.name,
            'description': self.description,
            'provider': self.provider,
            'model': self.model,
            'system_prompt': self.system_prompt,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'behavior_config': self.behavior_config or {},
            'is_default': self.is_default,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

