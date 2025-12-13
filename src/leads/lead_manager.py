"""
Lead Manager
Gerencia leads no banco de dados
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
import logging

from src.models.lead import Lead, LeadStatus
from src.database.db import SessionLocal

logger = logging.getLogger(__name__)


class LeadManager:
    """Gerencia leads"""
    
    def __init__(self, db: Optional[Session] = None):
        """
        Inicializa o manager
        
        Args:
            db: Sessão do banco (opcional, cria nova se não fornecido)
        """
        self.db = db
    
    def _get_db(self) -> Session:
        """Obtém sessão do banco"""
        if self.db:
            return self.db
        return SessionLocal()
    
    def create_lead(
        self,
        tenant_id: int,
        phone: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        source: Optional[str] = None,
        source_details: Optional[Dict[str, Any]] = None,
        score: float = 0.0,
        status: LeadStatus = LeadStatus.NEW,
        conversation_id: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
    ) -> Lead:
        """
        Cria um novo lead
        
        Args:
            tenant_id: ID do tenant
            phone: Número do telefone
            name: Nome do lead
            email: Email do lead
            source: Origem (flow, manual, api, etc)
            source_details: Detalhes da origem
            score: Pontuação (0-100)
            status: Status do lead
            conversation_id: ID da conversa relacionada
            metadata: Dados adicionais
            tags: Tags do lead
        
        Returns:
            Lead criado
        """
        db = self._get_db()
        try:
            # Verifica se já existe lead com esse telefone
            existing = db.query(Lead).filter(
                Lead.tenant_id == tenant_id,
                Lead.phone == phone
            ).first()
            
            if existing:
                # Atualiza lead existente
                if name and not existing.name:
                    existing.name = name
                if email and not existing.email:
                    existing.email = email
                if conversation_id:
                    existing.conversation_id = conversation_id
                if source:
                    existing.source = source
                if source_details:
                    existing.source_details = source_details
                if metadata:
                    existing.extra_data = {**(existing.extra_data or {}), **metadata}
                if tags:
                    existing_tags = existing.tags or []
                    for tag in tags:
                        if tag not in existing_tags:
                            existing_tags.append(tag)
                    existing.tags = existing_tags
                
                existing.last_contact_at = datetime.utcnow()
                existing.updated_at = datetime.utcnow()
                
                db.commit()
                db.refresh(existing)
                
                logger.info(f"Lead existente {existing.id} atualizado para {phone}")
                return existing
            
            # Cria novo lead
            lead = Lead(
                tenant_id=tenant_id,
                phone=phone,
                name=name,
                email=email,
                source=source,
                source_details=source_details or {},
                score=score,
                status=status,
                conversation_id=conversation_id,
                metadata=metadata or {},
                tags=tags or [],
                first_contact_at=datetime.utcnow(),
                last_contact_at=datetime.utcnow()
            )
            
            db.add(lead)
            db.commit()
            db.refresh(lead)
            
            logger.info(f"Lead {lead.id} criado para {phone}")
            return lead
            
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao criar lead: {e}")
            raise
        finally:
            if not self.db:
                db.close()
    
    def get_lead(self, lead_id: int) -> Optional[Lead]:
        """
        Busca um lead por ID
        
        Args:
            lead_id: ID do lead
        
        Returns:
            Lead ou None
        """
        db = self._get_db()
        try:
            return db.query(Lead).filter(Lead.id == lead_id).first()
        except Exception as e:
            logger.error(f"Erro ao buscar lead {lead_id}: {e}")
            return None
        finally:
            if not self.db:
                db.close()
    
    def get_lead_by_phone(self, tenant_id: int, phone: str) -> Optional[Lead]:
        """
        Busca lead por telefone
        
        Args:
            tenant_id: ID do tenant
            phone: Número do telefone
        
        Returns:
            Lead ou None
        """
        db = self._get_db()
        try:
            return db.query(Lead).filter(
                Lead.tenant_id == tenant_id,
                Lead.phone == phone
            ).first()
        except Exception as e:
            logger.error(f"Erro ao buscar lead por telefone: {e}")
            return None
        finally:
            if not self.db:
                db.close()
    
    def get_leads(
        self,
        tenant_id: Optional[int] = None,
        status: Optional[LeadStatus] = None,
        source: Optional[str] = None,
        search: Optional[str] = None,
        min_score: Optional[float] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Lead]:
        """
        Busca leads
        
        Args:
            tenant_id: Filtrar por tenant
            status: Filtrar por status
            source: Filtrar por origem
            search: Busca por nome, telefone ou email
            min_score: Pontuação mínima
            limit: Limite de resultados
            offset: Offset para paginação
        
        Returns:
            Lista de leads
        """
        db = self._get_db()
        try:
            query = db.query(Lead)
            
            if tenant_id:
                query = query.filter(Lead.tenant_id == tenant_id)
            
            if status:
                query = query.filter(Lead.status == status)
            
            if source:
                query = query.filter(Lead.source == source)
            
            if min_score is not None:
                query = query.filter(Lead.score >= min_score)
            
            if search:
                search_term = f"%{search}%"
                query = query.filter(
                    or_(
                        Lead.name.ilike(search_term),
                        Lead.phone.ilike(search_term),
                        Lead.email.ilike(search_term)
                    )
                )
            
            query = query.order_by(desc(Lead.created_at))
            query = query.limit(limit).offset(offset)
            
            return query.all()
            
        except Exception as e:
            logger.error(f"Erro ao buscar leads: {e}")
            return []
        finally:
            if not self.db:
                db.close()
    
    def update_lead(
        self,
        lead_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        score: Optional[float] = None,
        status: Optional[LeadStatus] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
    ) -> bool:
        """
        Atualiza um lead
        
        Args:
            lead_id: ID do lead
            name: Nome
            email: Email
            score: Pontuação
            status: Status
            metadata: Dados adicionais
            tags: Tags
        
        Returns:
            True se atualizado
        """
        db = self._get_db()
        try:
            lead = db.query(Lead).filter(Lead.id == lead_id).first()
            if not lead:
                return False
            
            if name is not None:
                lead.name = name
            if email is not None:
                lead.email = email
            if score is not None:
                lead.score = score
            if status is not None:
                lead.status = status
            if metadata is not None:
                lead.extra_data = {**(lead.extra_data or {}), **metadata}
            if tags is not None:
                lead.tags = tags
            
            lead.updated_at = datetime.utcnow()
            
            db.commit()
            logger.info(f"Lead {lead_id} atualizado")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao atualizar lead {lead_id}: {e}")
            return False
        finally:
            if not self.db:
                db.close()
    
    def update_status(self, lead_id: int, status: LeadStatus) -> bool:
        """
        Atualiza status do lead
        
        Args:
            lead_id: ID do lead
            status: Novo status
        
        Returns:
            True se atualizado
        """
        db = self._get_db()
        try:
            lead = db.query(Lead).filter(Lead.id == lead_id).first()
            if not lead:
                return False
            
            lead.status = status
            lead.updated_at = datetime.utcnow()
            
            # Se converter, marca data de conversão
            if status == LeadStatus.CONVERTED:
                lead.converted_at = datetime.utcnow()
            
            db.commit()
            logger.info(f"Lead {lead_id} atualizado para status {status.value}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao atualizar status do lead {lead_id}: {e}")
            return False
        finally:
            if not self.db:
                db.close()
    
    def delete_lead(self, lead_id: int) -> bool:
        """
        Deleta um lead
        
        Args:
            lead_id: ID do lead
        
        Returns:
            True se deletado
        """
        db = self._get_db()
        try:
            lead = db.query(Lead).filter(Lead.id == lead_id).first()
            if not lead:
                return False
            
            db.delete(lead)
            db.commit()
            logger.info(f"Lead {lead_id} deletado")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao deletar lead {lead_id}: {e}")
            return False
        finally:
            if not self.db:
                db.close()
    
    def get_stats(self, tenant_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Retorna estatísticas de leads
        
        Args:
            tenant_id: Filtrar por tenant
        
        Returns:
            Dict com estatísticas
        """
        db = self._get_db()
        try:
            query = db.query(Lead)
            if tenant_id:
                query = query.filter(Lead.tenant_id == tenant_id)
            
            all_leads = query.all()
            
            stats = {
                'total': len(all_leads),
                'by_status': {},
                'by_source': {},
                'average_score': 0.0,
                'new_today': 0,
                'converted': 0
            }
            
            total_score = 0
            today = datetime.utcnow().date()
            
            for lead in all_leads:
                # Por status
                status_key = lead.status.value
                stats['by_status'][status_key] = stats['by_status'].get(status_key, 0) + 1
                
                # Por origem
                source_key = lead.source or 'unknown'
                stats['by_source'][source_key] = stats['by_source'].get(source_key, 0) + 1
                
                # Score
                total_score += lead.score
                
                # Novos hoje
                if lead.created_at.date() == today:
                    stats['new_today'] += 1
                
                # Convertidos
                if lead.status == LeadStatus.CONVERTED:
                    stats['converted'] += 1
            
            if len(all_leads) > 0:
                stats['average_score'] = total_score / len(all_leads)
            
            return stats
            
        except Exception as e:
            logger.error(f"Erro ao buscar estatísticas: {e}")
            return {}
        finally:
            if not self.db:
                db.close()
