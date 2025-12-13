"""
Models: Subscription e Plan
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from src.database.db import Base


class SubscriptionStatus(enum.Enum):
    """Status da assinatura"""
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    TRIAL = "trial"
    PENDING = "pending"


class Plan(Base):
    """Plano de assinatura"""
    __tablename__ = 'plans'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    currency = Column(String(3), default='BRL', nullable=False)
    
    # Limites
    max_instances = Column(Integer, default=1, nullable=False)  # -1 = ilimitado
    max_flows = Column(Integer, default=3, nullable=False)
    max_messages_month = Column(Integer, default=1000, nullable=False)
    
    # Features (JSON array)
    features = Column(JSON, default=list, nullable=False)
    
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relacionamentos
    tenants = relationship("Tenant", back_populates="plan")
    subscriptions = relationship("Subscription", back_populates="plan")
    
    def __repr__(self):
        return f"<Plan(id={self.id}, name={self.name}, price={self.price})>"


class Subscription(Base):
    """Assinatura de um tenant"""
    __tablename__ = 'subscriptions'
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), unique=True, nullable=False)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.TRIAL, nullable=False)
    
    # Datas
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime, nullable=True)
    trial_end_date = Column(DateTime, nullable=True)
    
    # Pagamento
    payment_method = Column(String(50), nullable=True)  # stripe, mercadopago, asaas
    payment_id = Column(String(255), nullable=True)  # ID no gateway
    payment_status = Column(String(50), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    tenant = relationship("Tenant", back_populates="subscription")
    plan = relationship("Plan", back_populates="subscriptions")
    
    def __repr__(self):
        return f"<Subscription(id={self.id}, tenant_id={self.tenant_id}, status={self.status.value})>"
