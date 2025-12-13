"""
API de Leads
Endpoints para gerenciar leads
"""
from flask import Blueprint, request, jsonify
from typing import Optional
import logging

from src.leads.lead_manager import LeadManager
from src.models.lead import LeadStatus
from src.database.db import SessionLocal

logger = logging.getLogger(__name__)

bp = Blueprint('leads', __name__, url_prefix='/api/leads')


@bp.route('', methods=['GET'])
def list_leads():
    """
    Lista leads
    
    Query params:
        - tenant_id: Filtrar por tenant
        - status: Filtrar por status (new, contacted, qualified, converted, lost)
        - source: Filtrar por origem
        - search: Busca por nome, telefone ou email
        - min_score: Pontuação mínima
        - limit: Limite de resultados (padrão: 50)
        - offset: Offset para paginação (padrão: 0)
    """
    try:
        manager = LeadManager()
        
        tenant_id = request.args.get('tenant_id', type=int)
        status_str = request.args.get('status')
        source = request.args.get('source')
        search = request.args.get('search')
        min_score = request.args.get('min_score', type=float)
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Converte status string para enum
        status = None
        if status_str:
            try:
                status = LeadStatus(status_str)
            except ValueError:
                pass
        
        leads = manager.get_leads(
            tenant_id=tenant_id,
            status=status,
            source=source,
            search=search,
            min_score=min_score,
            limit=limit,
            offset=offset
        )
        
        return jsonify({
            'success': True,
            'leads': [
                {
                    'id': l.id,
                    'phone': l.phone,
                    'name': l.name,
                    'email': l.email,
                    'source': l.source,
                    'score': l.score,
                    'status': l.status.value,
                    'tags': l.tags or [],
                    'conversation_id': l.conversation_id,
                    'first_contact_at': l.first_contact_at.isoformat() if l.first_contact_at else None,
                    'last_contact_at': l.last_contact_at.isoformat() if l.last_contact_at else None,
                    'converted_at': l.converted_at.isoformat() if l.converted_at else None,
                    'metadata': l.extra_data or {},
                    'created_at': l.created_at.isoformat()
                }
                for l in leads
            ],
            'count': len(leads)
        })
        
    except Exception as e:
        logger.error(f"Erro ao listar leads: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/<int:lead_id>', methods=['GET'])
def get_lead(lead_id: int):
    """Busca um lead por ID"""
    try:
        manager = LeadManager()
        lead = manager.get_lead(lead_id)
        
        if not lead:
            return jsonify({
                'success': False,
                'error': 'Lead não encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'lead': {
                'id': lead.id,
                'phone': lead.phone,
                'name': lead.name,
                'email': lead.email,
                'source': lead.source,
                'source_details': lead.source_details or {},
                'score': lead.score,
                'status': lead.status.value,
                'tags': lead.tags or [],
                'conversation_id': lead.conversation_id,
                'first_contact_at': lead.first_contact_at.isoformat() if lead.first_contact_at else None,
                'last_contact_at': lead.last_contact_at.isoformat() if lead.last_contact_at else None,
                'converted_at': lead.converted_at.isoformat() if lead.converted_at else None,
                'metadata': lead.extra_data or {},
                'created_at': lead.created_at.isoformat(),
                'updated_at': lead.updated_at.isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar lead: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('', methods=['POST'])
def create_lead():
    """
    Cria um novo lead
    
    Body:
        - tenant_id: ID do tenant
        - phone: Número do telefone
        - name: Nome (opcional)
        - email: Email (opcional)
        - source: Origem (opcional)
        - source_details: Detalhes da origem (opcional)
        - tags: Tags (opcional)
    """
    try:
        data = request.get_json()
        
        tenant_id = data.get('tenant_id', 1)
        phone = data.get('phone')
        name = data.get('name')
        email = data.get('email')
        source = data.get('source', 'manual')
        source_details = data.get('source_details', {})
        tags = data.get('tags', [])
        
        if not phone:
            return jsonify({
                'success': False,
                'error': 'phone é obrigatório'
            }), 400
        
        manager = LeadManager()
        
        lead = manager.create_lead(
            tenant_id=tenant_id,
            phone=phone,
            name=name,
            email=email,
            source=source,
            source_details=source_details,
            tags=tags
        )
        
        return jsonify({
            'success': True,
            'lead': {
                'id': lead.id,
                'phone': lead.phone,
                'name': lead.name,
                'email': lead.email,
                'score': lead.score,
                'status': lead.status.value,
                'created_at': lead.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Erro ao criar lead: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/<int:lead_id>', methods=['PUT'])
def update_lead(lead_id: int):
    """
    Atualiza um lead
    
    Body:
        - name: Nome (opcional)
        - email: Email (opcional)
        - score: Pontuação (opcional)
        - status: Status (opcional)
        - tags: Tags (opcional)
    """
    try:
        data = request.get_json()
        
        manager = LeadManager()
        
        # Converte status string para enum
        status = None
        if data.get('status'):
            try:
                status = LeadStatus(data['status'])
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': f'Status inválido: {data["status"]}'
                }), 400
        
        success = manager.update_lead(
            lead_id=lead_id,
            name=data.get('name'),
            email=data.get('email'),
            score=data.get('score'),
            status=status,
            tags=data.get('tags')
        )
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Lead não encontrado'
            }), 404
        
        lead = manager.get_lead(lead_id)
        
        return jsonify({
            'success': True,
            'lead': {
                'id': lead.id,
                'phone': lead.phone,
                'name': lead.name,
                'email': lead.email,
                'score': lead.score,
                'status': lead.status.value,
                'tags': lead.tags or []
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao atualizar lead: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/<int:lead_id>/status', methods=['PUT'])
def update_lead_status(lead_id: int):
    """
    Atualiza status de um lead
    
    Body:
        - status: Novo status (new, contacted, qualified, converted, lost)
    """
    try:
        data = request.get_json()
        status_str = data.get('status')
        
        if not status_str:
            return jsonify({
                'success': False,
                'error': 'status é obrigatório'
            }), 400
        
        try:
            status = LeadStatus(status_str)
        except ValueError:
            return jsonify({
                'success': False,
                'error': f'Status inválido: {status_str}'
            }), 400
        
        manager = LeadManager()
        success = manager.update_status(lead_id, status)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Lead não encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'message': f'Status atualizado para {status.value}'
        })
        
    except Exception as e:
        logger.error(f"Erro ao atualizar status do lead: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/<int:lead_id>', methods=['DELETE'])
def delete_lead(lead_id: int):
    """Deleta um lead"""
    try:
        manager = LeadManager()
        success = manager.delete_lead(lead_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Lead não encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Lead deletado'
        })
        
    except Exception as e:
        logger.error(f"Erro ao deletar lead: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Retorna estatísticas de leads
    
    Query params:
        - tenant_id: Filtrar por tenant (opcional)
    """
    try:
        tenant_id = request.args.get('tenant_id', type=int)
        manager = LeadManager()
        
        stats = manager.get_stats(tenant_id=tenant_id)
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar estatísticas: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
