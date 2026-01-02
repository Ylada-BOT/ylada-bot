"""
Model: IAUsage (Rastreamento de uso de IA)
"""
from sqlalchemy import Column, Integer, Float, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime, date
from src.database.db import Base


class IAUsage(Base):
    """Rastreamento de uso de IA por tenant"""
    __tablename__ = 'ia_usage'
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)
    instance_id = Column(Integer, ForeignKey('instances.id'), nullable=True, index=True)
    
    # Data do uso
    date = Column(Date, nullable=False, default=date.today, index=True)
    
    # Métricas
    messages_count = Column(Integer, default=0, nullable=False)  # Número de mensagens processadas
    tokens_used = Column(Integer, default=0, nullable=False)  # Tokens consumidos
    cost = Column(Float, default=0.0, nullable=False)  # Custo real em R$
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    tenant = relationship("Tenant", backref="ia_usage_records")
    instance = relationship("Instance", backref="ia_usage_records")
    
    # Índices compostos para queries eficientes
    __table_args__ = (
        Index('idx_tenant_date', 'tenant_id', 'date'),
        Index('idx_tenant_instance_date', 'tenant_id', 'instance_id', 'date'),
    )
    
    def __repr__(self):
        return f"<IAUsage(tenant_id={self.tenant_id}, date={self.date}, messages={self.messages_count})>"





