"""
Model: UsageLimits (Limites de uso por tenant)
"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime, date
from src.database.db import Base


class UsageLimits(Base):
    """Limites de uso mensal por tenant"""
    __tablename__ = 'usage_limits'
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), unique=True, nullable=False, index=True)
    
    # Contador do mês atual
    current_month_messages = Column(Integer, default=0, nullable=False)
    
    # Data de reset (primeiro dia do próximo mês)
    limit_reset_date = Column(Date, nullable=False)
    
    # Timestamps
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relacionamento
    tenant = relationship("Tenant", backref="usage_limits", uselist=False)
    
    def __repr__(self):
        return f"<UsageLimits(tenant_id={self.tenant_id}, messages={self.current_month_messages})>"
    
    def needs_reset(self) -> bool:
        """Verifica se precisa resetar (novo mês)"""
        return date.today() >= self.limit_reset_date
    
    def reset(self):
        """Reseta contador para novo mês"""
        from datetime import timedelta
        from calendar import monthrange
        
        today = date.today()
        # Próximo mês
        if today.month == 12:
            next_month = date(today.year + 1, 1, 1)
        else:
            next_month = date(today.year, today.month + 1, 1)
        
        self.current_month_messages = 0
        self.limit_reset_date = next_month
        self.last_updated = datetime.utcnow()


