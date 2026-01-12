"""
API para gerenciar conversas - Funcionalidades avançadas
Baseado na análise do BotConversa
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from src.database.db import SessionLocal
from src.models.conversation import Conversation, ConversationStatus
from src.models.user import User
from web.utils.auth_helpers import get_current_user_id, get_current_tenant_id, require_api_auth
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('conversations_api', __name__, url_prefix='/api/conversations')


@bp.route('/<chat_id>/status', methods=['PUT'])
@require_api_auth
def update_conversation_status(chat_id):
    """
    Atualiza status de uma conversa
    
    Body:
        - status: "open", "closed", "archived"
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
            status = ConversationStatus(status_str)
        except ValueError:
            return jsonify({
                'success': False,
                'error': f'Status inválido: {status_str}. Use: open, closed, archived'
            }), 400
        
        db = SessionLocal()
        try:
            # Busca conversa pelo phone (chat_id pode ser o phone do WhatsApp)
            # Primeiro tenta buscar pelo ID se for numérico
            conversation = None
            if chat_id.isdigit():
                conversation = db.query(Conversation).filter(Conversation.id == int(chat_id)).first()
            
            # Se não encontrou, busca pelo phone
            if not conversation:
                tenant_id = get_current_tenant_id()
                conversation = db.query(Conversation).filter(
                    Conversation.phone == chat_id,
                    Conversation.tenant_id == tenant_id
                ).first()
            
            if not conversation:
                return jsonify({
                    'success': False,
                    'error': 'Conversa não encontrada'
                }), 404
            
            # Atualiza status
            conversation.status = status
            conversation.updated_at = datetime.utcnow()
            db.commit()
            
            return jsonify({
                'success': True,
                'conversation': {
                    'id': conversation.id,
                    'phone': conversation.phone,
                    'status': conversation.status.value
                }
            })
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao atualizar status da conversa: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/<chat_id>/assign', methods=['PUT'])
@require_api_auth
def assign_conversation(chat_id):
    """
    Atribui uma conversa a um usuário/agente
    
    Body:
        - user_id: ID do usuário (ou null para desatribuir)
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        db = SessionLocal()
        try:
            # Busca conversa
            conversation = None
            if chat_id.isdigit():
                conversation = db.query(Conversation).filter(Conversation.id == int(chat_id)).first()
            
            if not conversation:
                tenant_id = get_current_tenant_id()
                conversation = db.query(Conversation).filter(
                    Conversation.phone == chat_id,
                    Conversation.tenant_id == tenant_id
                ).first()
            
            if not conversation:
                return jsonify({
                    'success': False,
                    'error': 'Conversa não encontrada'
                }), 404
            
            # Se user_id fornecido, verifica se existe
            if user_id:
                user = db.query(User).filter(User.id == user_id).first()
                if not user:
                    return jsonify({
                        'success': False,
                        'error': 'Usuário não encontrado'
                    }), 404
            
            # Atualiza atribuição
            conversation.assigned_to = user_id
            conversation.updated_at = datetime.utcnow()
            db.commit()
            
            # Busca nome do usuário se atribuído
            assigned_user_name = None
            if user_id:
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    assigned_user_name = user.name or user.email
            
            return jsonify({
                'success': True,
                'conversation': {
                    'id': conversation.id,
                    'phone': conversation.phone,
                    'assigned_to': conversation.assigned_to,
                    'assigned_user_name': assigned_user_name
                }
            })
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao atribuir conversa: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/<chat_id>/tags', methods=['PUT'])
@require_api_auth
def update_conversation_tags(chat_id):
    """
    Atualiza tags de uma conversa
    
    Body:
        - tags: Array de strings (ex: ["VIP", "Reclamação"])
    """
    try:
        data = request.get_json()
        tags = data.get('tags', [])
        
        if not isinstance(tags, list):
            return jsonify({
                'success': False,
                'error': 'tags deve ser um array'
            }), 400
        
        db = SessionLocal()
        try:
            # Busca conversa
            conversation = None
            if chat_id.isdigit():
                conversation = db.query(Conversation).filter(Conversation.id == int(chat_id)).first()
            
            if not conversation:
                tenant_id = get_current_tenant_id()
                conversation = db.query(Conversation).filter(
                    Conversation.phone == chat_id,
                    Conversation.tenant_id == tenant_id
                ).first()
            
            if not conversation:
                return jsonify({
                    'success': False,
                    'error': 'Conversa não encontrada'
                }), 404
            
            # Atualiza tags
            conversation.tags = tags
            conversation.updated_at = datetime.utcnow()
            db.commit()
            
            return jsonify({
                'success': True,
                'conversation': {
                    'id': conversation.id,
                    'phone': conversation.phone,
                    'tags': conversation.tags or []
                }
            })
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao atualizar tags da conversa: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/<chat_id>/automation', methods=['PUT'])
@require_api_auth
def toggle_conversation_automation(chat_id):
    """
    Liga/desliga automação para uma conversa
    
    Body:
        - enabled: true/false
    """
    try:
        data = request.get_json()
        enabled = data.get('enabled')
        
        if enabled is None:
            return jsonify({
                'success': False,
                'error': 'enabled é obrigatório (true/false)'
            }), 400
        
        db = SessionLocal()
        try:
            # Busca conversa
            conversation = None
            if chat_id.isdigit():
                conversation = db.query(Conversation).filter(Conversation.id == int(chat_id)).first()
            
            if not conversation:
                tenant_id = get_current_tenant_id()
                conversation = db.query(Conversation).filter(
                    Conversation.phone == chat_id,
                    Conversation.tenant_id == tenant_id
                ).first()
            
            if not conversation:
                return jsonify({
                    'success': False,
                    'error': 'Conversa não encontrada'
                }), 404
            
            # Atualiza automação
            conversation.automation_enabled = bool(enabled)
            conversation.updated_at = datetime.utcnow()
            db.commit()
            
            return jsonify({
                'success': True,
                'conversation': {
                    'id': conversation.id,
                    'phone': conversation.phone,
                    'automation_enabled': conversation.automation_enabled
                }
            })
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao atualizar automação da conversa: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/<chat_id>/details', methods=['GET'])
@require_api_auth
def get_conversation_details(chat_id):
    """
    Obtém detalhes completos de uma conversa
    """
    try:
        db = SessionLocal()
        try:
            # Busca conversa
            conversation = None
            if chat_id.isdigit():
                conversation = db.query(Conversation).filter(Conversation.id == int(chat_id)).first()
            
            if not conversation:
                tenant_id = get_current_tenant_id()
                conversation = db.query(Conversation).filter(
                    Conversation.phone == chat_id,
                    Conversation.tenant_id == tenant_id
                ).first()
            
            if not conversation:
                return jsonify({
                    'success': False,
                    'error': 'Conversa não encontrada'
                }), 404
            
            # Busca informações do usuário atribuído
            assigned_user = None
            if conversation.assigned_to:
                user = db.query(User).filter(User.id == conversation.assigned_to).first()
                if user:
                    assigned_user = {
                        'id': user.id,
                        'name': user.name or user.email,
                        'email': user.email
                    }
            
            # Busca informações do lead se houver
            lead_info = None
            if conversation.lead_id and conversation.lead:
                lead = conversation.lead
                lead_info = {
                    'id': lead.id,
                    'name': lead.name,
                    'email': lead.email,
                    'score': lead.score,
                    'status': lead.status.value if lead.status else None,
                    'tags': lead.tags or []
                }
            
            return jsonify({
                'success': True,
                'conversation': {
                    'id': conversation.id,
                    'phone': conversation.phone,
                    'contact_name': conversation.contact_name,
                    'contact_email': conversation.contact_email,
                    'contact_cpf': conversation.contact_cpf,
                    'status': conversation.status.value if conversation.status else 'open',
                    'assigned_to': conversation.assigned_to,
                    'assigned_user': assigned_user,
                    'tags': conversation.tags or [],
                    'automation_enabled': conversation.automation_enabled if hasattr(conversation, 'automation_enabled') else True,
                    'message_count': conversation.message_count,
                    'unread_count': conversation.unread_count,
                    'last_message_at': conversation.last_message_at.isoformat() if conversation.last_message_at else None,
                    'lead': lead_info,
                    'created_at': conversation.created_at.isoformat() if conversation.created_at else None,
                    'updated_at': conversation.updated_at.isoformat() if conversation.updated_at else None
                }
            })
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao buscar detalhes da conversa: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/<chat_id>/update', methods=['PUT'])
@require_api_auth
def update_conversation(chat_id):
    """
    Atualiza informações gerais de uma conversa
    
    Body (todos opcionais):
        - contact_name: Nome do contato
        - contact_email: Email do contato
        - contact_cpf: CPF do contato
        - status: Status da conversa
        - assigned_to: ID do usuário atribuído
        - tags: Array de tags
        - automation_enabled: true/false
    """
    try:
        data = request.get_json()
        
        db = SessionLocal()
        try:
            # Busca conversa
            conversation = None
            if chat_id.isdigit():
                conversation = db.query(Conversation).filter(Conversation.id == int(chat_id)).first()
            
            if not conversation:
                tenant_id = get_current_tenant_id()
                conversation = db.query(Conversation).filter(
                    Conversation.phone == chat_id,
                    Conversation.tenant_id == tenant_id
                ).first()
            
            if not conversation:
                return jsonify({
                    'success': False,
                    'error': 'Conversa não encontrada'
                }), 404
            
            # Atualiza campos fornecidos
            if 'contact_name' in data:
                conversation.contact_name = data['contact_name']
            if 'contact_email' in data:
                conversation.contact_email = data['contact_email']
            if 'contact_cpf' in data:
                conversation.contact_cpf = data['contact_cpf']
            if 'status' in data:
                try:
                    conversation.status = ConversationStatus(data['status'])
                except ValueError:
                    return jsonify({
                        'success': False,
                        'error': f'Status inválido: {data["status"]}'
                    }), 400
            if 'assigned_to' in data:
                conversation.assigned_to = data['assigned_to']
            if 'tags' in data:
                conversation.tags = data['tags']
            if 'automation_enabled' in data:
                conversation.automation_enabled = bool(data['automation_enabled'])
            
            conversation.updated_at = datetime.utcnow()
            db.commit()
            
            return jsonify({
                'success': True,
                'conversation': {
                    'id': conversation.id,
                    'phone': conversation.phone,
                    'contact_name': conversation.contact_name,
                    'contact_email': conversation.contact_email,
                    'contact_cpf': conversation.contact_cpf,
                    'status': conversation.status.value if conversation.status else 'open',
                    'assigned_to': conversation.assigned_to,
                    'tags': conversation.tags or [],
                    'automation_enabled': conversation.automation_enabled if hasattr(conversation, 'automation_enabled') else True
                }
            })
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao atualizar conversa: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

