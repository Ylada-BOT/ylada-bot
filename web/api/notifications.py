"""
API de Notificações
Endpoints para gerenciar notificações
"""
from flask import Blueprint, request, jsonify
from typing import Optional
import logging

from src.notifications.notification_manager import NotificationManager
from src.notifications.notification_sender import NotificationSender
from src.models.notification import NotificationType, NotificationStatus
from src.database.db import SessionLocal
from web.utils.auth_helpers import get_current_tenant_id, is_admin
from web.utils.rate_limiter import rate_limit_whatsapp

logger = logging.getLogger(__name__)

bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')


def get_notification_sender():
    """Obtém instância do NotificationSender"""
    try:
        from web.app import whatsapp
        return NotificationSender(whatsapp)
    except:
        return None


@bp.route('', methods=['GET'])
def list_notifications():
    """
    Lista notificações
    
    Query params:
        - tenant_id: Filtrar por tenant
        - type: Filtrar por tipo (lead_captured, flow_triggered, etc)
        - status: Filtrar por status (pending, sent, failed)
        - limit: Limite de resultados (padrão: 50)
        - offset: Offset para paginação (padrão: 0)
    """
    try:
        manager = NotificationManager()
        
        # Obtém tenant_id do usuário atual (ou do parâmetro se for admin)
        current_tenant_id = get_current_tenant_id()
        requested_tenant_id = request.args.get('tenant_id', type=int)
        
        # Admin pode ver todos ou filtrar por tenant_id
        if is_admin():
            tenant_id = requested_tenant_id  # Admin pode escolher qual tenant ver
        else:
            # Tenant só vê suas próprias notificações
            tenant_id = current_tenant_id
            if not tenant_id:
                return jsonify({
                    'success': True,
                    'notifications': [],
                    'total': 0
                }), 200
        notification_type = request.args.get('type')
        status = request.args.get('status')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Converte string para enum se fornecido
        notification_type_enum = None
        if notification_type:
            try:
                notification_type_enum = NotificationType(notification_type)
            except ValueError:
                pass
        
        status_enum = None
        if status:
            try:
                status_enum = NotificationStatus(status)
            except ValueError:
                pass
        
        notifications = manager.get_notifications(
            tenant_id=tenant_id,
            notification_type=notification_type_enum,
            status=status_enum,
            limit=limit,
            offset=offset
        )
        
        return jsonify({
            'success': True,
            'notifications': [
                {
                    'id': n.id,
                    'type': n.type.value,
                    'title': n.title,
                    'message': n.message,
                    'sent_to': n.sent_to,
                    'sent_to_name': n.sent_to_name,
                    'status': n.status.value,
                    'sent_at': n.sent_at.isoformat() if n.sent_at else None,
                    'error_message': n.error_message,
                    'related_lead_id': n.related_lead_id,
                    'related_conversation_id': n.related_conversation_id,
                    'related_flow_id': n.related_flow_id,
                    'metadata': n.extra_data or {},
                    'created_at': n.created_at.isoformat()
                }
                for n in notifications
            ],
            'count': len(notifications)
        })
        
    except Exception as e:
        logger.error(f"Erro ao listar notificações: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/<int:notification_id>', methods=['GET'])
def get_notification(notification_id: int):
    """Busca uma notificação por ID"""
    try:
        manager = NotificationManager()
        notification = manager.get_notification(notification_id)
        
        if not notification:
            return jsonify({
                'success': False,
                'error': 'Notificação não encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'notification': {
                'id': notification.id,
                'type': notification.type.value,
                'title': notification.title,
                'message': notification.message,
                'sent_to': notification.sent_to,
                'sent_to_name': notification.sent_to_name,
                'status': notification.status.value,
                'sent_at': notification.sent_at.isoformat() if notification.sent_at else None,
                'error_message': notification.error_message,
                'related_lead_id': notification.related_lead_id,
                'related_conversation_id': notification.related_conversation_id,
                'related_flow_id': notification.related_flow_id,
                'metadata': notification.extra_data or {},
                'created_at': notification.created_at.isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar notificação: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('', methods=['POST'])
def create_notification():
    """
    Cria uma nova notificação
    
    Body:
        - tenant_id: ID do tenant
        - type: Tipo da notificação (lead_captured, flow_triggered, custom, etc)
        - message: Mensagem
        - sent_to: Número WhatsApp destino
        - title: Título (opcional)
        - sent_to_name: Nome do destinatário (opcional)
        - related_lead_id: ID do lead relacionado (opcional)
        - related_conversation_id: ID da conversa relacionada (opcional)
        - related_flow_id: ID do fluxo relacionado (opcional)
        - metadata: Dados adicionais (opcional)
        - send_immediately: Se True, envia imediatamente (padrão: True)
    """
    try:
        data = request.get_json()
        
        tenant_id = data.get('tenant_id', 1)  # Default tenant 1
        notification_type_str = data.get('type', 'custom')
        message = data.get('message')
        sent_to = data.get('sent_to')
        title = data.get('title')
        sent_to_name = data.get('sent_to_name')
        related_lead_id = data.get('related_lead_id')
        related_conversation_id = data.get('related_conversation_id')
        related_flow_id = data.get('related_flow_id')
        metadata = data.get('metadata', {})
        send_immediately = data.get('send_immediately', True)
        
        if not message or not sent_to:
            return jsonify({
                'success': False,
                'error': 'message e sent_to são obrigatórios'
            }), 400
        
        # Converte tipo
        try:
            notification_type = NotificationType(notification_type_str)
        except ValueError:
            return jsonify({
                'success': False,
                'error': f'Tipo inválido: {notification_type_str}'
            }), 400
        
        manager = NotificationManager()
        
        notification = manager.create_notification(
            tenant_id=tenant_id,
            notification_type=notification_type,
            message=message,
            sent_to=sent_to,
            title=title,
            sent_to_name=sent_to_name,
            related_lead_id=related_lead_id,
            related_conversation_id=related_conversation_id,
            related_flow_id=related_flow_id,
            metadata=metadata
        )
        
        # Envia imediatamente se solicitado
        if send_immediately:
            sender = get_notification_sender()
            if sender:
                sender.send_notification(notification)
            else:
                logger.warning("NotificationSender não disponível, notificação ficará pendente")
        
        return jsonify({
            'success': True,
            'notification': {
                'id': notification.id,
                'type': notification.type.value,
                'status': notification.status.value,
                'created_at': notification.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Erro ao criar notificação: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/<int:notification_id>/send', methods=['POST'])
@rate_limit_whatsapp  # Rate limiting para envio de notificações
def send_notification(notification_id: int):
    """Envia uma notificação pendente"""
    try:
        manager = NotificationManager()
        notification = manager.get_notification(notification_id)
        
        if not notification:
            return jsonify({
                'success': False,
                'error': 'Notificação não encontrada'
            }), 404
        
        if notification.status != NotificationStatus.PENDING:
            return jsonify({
                'success': False,
                'error': f'Notificação já foi processada (status: {notification.status.value})'
            }), 400
        
        sender = get_notification_sender()
        if not sender:
            return jsonify({
                'success': False,
                'error': 'NotificationSender não disponível'
            }), 503
        
        success = sender.send_notification(notification)
        
        return jsonify({
            'success': success,
            'notification': {
                'id': notification.id,
                'status': notification.status.value
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao enviar notificação: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/pending/send-all', methods=['POST'])
@rate_limit_whatsapp  # Rate limiting para envio em massa
def send_all_pending():
    """
    Envia todas as notificações pendentes
    
    Query params:
        - tenant_id: Filtrar por tenant (opcional)
    """
    try:
        tenant_id = request.args.get('tenant_id', type=int)
        
        sender = get_notification_sender()
        if not sender:
            return jsonify({
                'success': False,
                'error': 'NotificationSender não disponível'
            }), 503
        
        sent_count = sender.send_pending_notifications(tenant_id=tenant_id)
        
        return jsonify({
            'success': True,
            'sent_count': sent_count
        })
        
    except Exception as e:
        logger.error(f"Erro ao enviar notificações pendentes: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id: int):
    """Deleta uma notificação"""
    try:
        manager = NotificationManager()
        success = manager.delete_notification(notification_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Notificação não encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Notificação deletada'
        })
        
    except Exception as e:
        logger.error(f"Erro ao deletar notificação: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Retorna estatísticas de notificações
    
    Query params:
        - tenant_id: Filtrar por tenant (opcional)
    """
    try:
        tenant_id = request.args.get('tenant_id', type=int)
        manager = NotificationManager()
        
        # Busca todas as notificações do tenant
        all_notifications = manager.get_notifications(
            tenant_id=tenant_id,
            limit=1000  # Limite alto para estatísticas
        )
        
        stats = {
            'total': len(all_notifications),
            'pending': 0,
            'sent': 0,
            'failed': 0,
            'by_type': {}
        }
        
        for n in all_notifications:
            # Conta por status
            if n.status == NotificationStatus.PENDING:
                stats['pending'] += 1
            elif n.status == NotificationStatus.SENT:
                stats['sent'] += 1
            elif n.status == NotificationStatus.FAILED:
                stats['failed'] += 1
            
            # Conta por tipo
            type_key = n.type.value
            stats['by_type'][type_key] = stats['by_type'].get(type_key, 0) + 1
        
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
