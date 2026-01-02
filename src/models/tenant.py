"""
Model: Tenant (Cliente final - Multi-tenant)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from src.database.db import Base


class TenantStatus(enum.Enum):
    """Status do tenant"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"
    TRIAL = "trial"


class Tenant(Base):
    """Cliente final (multi-tenant)"""
    __tablename__ = 'tenants'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    subdomain = Column(String(100), unique=True, index=True, nullable=True)
    status = Column(Enum(TenantStatus), default=TenantStatus.TRIAL, nullable=False)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=True)
    
    # Bloqueio por exceder limite de IA
    is_blocked = Column(Boolean, default=False, nullable=False)  # Bloqueado por exceder hard limit
    blocked_reason = Column(String(500), nullable=True)  # Motivo do bloqueio
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    owner = relationship("User", back_populates="tenants")
    plan = relationship("Plan", back_populates="tenants")
    subscription = relationship("Subscription", back_populates="tenant", uselist=False)
    instances = relationship("Instance", back_populates="tenant", cascade="all, delete-orphan")
    flows = relationship("Flow", back_populates="tenant", cascade="all, delete-orphan")
    agents = relationship("Agent", back_populates="tenant", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="tenant", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="tenant", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="tenant", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Tenant(id={self.id}, name={self.name}, status={self.status.value})>"
