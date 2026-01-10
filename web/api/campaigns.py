"""
API para Campanhas de Envio em Massa
Similar ao Turbo Max, mas com IA e CRM integrado
"""
from flask import Blueprint, request, jsonify
from functools import wraps
import logging
from typing import List, Dict, Optional
import time
from datetime import datetime

logger = logging.getLogger(__name__)

bp = Blueprint('campaigns', __name__, url_prefix='/api/campaigns')


def require_api_auth(f):
    """Decorator para exigir autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import session
        from config.settings import AUTH_REQUIRED
        
        if not AUTH_REQUIRED:
            return f(*args, **kwargs)
        
        if 'user_id' not in session:
            return jsonify({'error': 'Não autenticado. Faça login primeiro.'}), 401
        
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/send-mass', methods=['POST'])
@require_api_auth
def send_mass_messages():
    """
    Envia mensagens em massa para uma lista de contatos
    
    Body JSON:
    {
        "contacts": ["5511999999999", "5511888888888", ...],
        "message": "Sua mensagem aqui",
        "instance_id": 1,  # opcional
        "delay_between_messages": 3,  # segundos entre cada mensagem (padrão: 3)
        "personalize": false,  # se true, substitui {nome} na mensagem
        "media_url": null  # opcional: URL de imagem/vídeo/áudio
    }
    """
    try:
        from flask import session
        from web.utils.instance_helper import get_or_create_user_instance
        from web.utils.auth_helpers import get_current_user_id
        from web.utils.message_queue import get_message_queue
        from web.utils.rate_limiter import rate_limit_whatsapp
        
        data = request.get_json()
        
        # Validação
        if not data:
            return jsonify({"success": False, "error": "Dados não fornecidos"}), 400
        
        contacts = data.get('contacts', [])
        message = data.get('message', '')
        instance_id = data.get('instance_id')
        delay = data.get('delay_between_messages', 3)  # Padrão: 3 segundos
        personalize = data.get('personalize', False)
        media_url = data.get('media_url')
        
        if not contacts or not isinstance(contacts, list):
            return jsonify({"success": False, "error": "Lista de contatos inválida"}), 400
        
        if not message or not message.strip():
            return jsonify({"success": False, "error": "Mensagem não pode estar vazia"}), 400
        
        if len(contacts) > 1000:
            return jsonify({
                "success": False,
                "error": "Limite de 1000 contatos por campanha. Use múltiplas campanhas para mais contatos."
            }), 400
        
        # Obtém instância
        user_id = get_current_user_id() or 1
        instance = get_or_create_user_instance(user_id, instance_id)
        if not instance:
            return jsonify({"success": False, "error": "Instância não encontrada"}), 404
        
        # Obtém fila de mensagens
        queue = get_message_queue()
        if not queue:
            return jsonify({"success": False, "error": "Sistema de fila não disponível"}), 503
        
        # Processa cada contato
        results = {
            "total": len(contacts),
            "added_to_queue": 0,
            "failed": 0,
            "message_ids": []
        }
        
        for i, contact in enumerate(contacts):
            try:
                # Formata número
                phone = str(contact).replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
                if not phone.startswith('55'):
                    # Assume que é número brasileiro sem código do país
                    phone = '55' + phone
                
                # Personaliza mensagem se solicitado
                personalized_message = message
                if personalize:
                    # Tenta obter nome do contato (se existir conversa)
                    try:
                        from src.database.db import SessionLocal
                        from src.models.conversation import Conversation
                        db = SessionLocal()
                        conv = db.query(Conversation).filter_by(
                            phone=phone,
                            instance_id=instance.get('id')
                        ).first()
                        if conv and conv.contact_name:
                            personalized_message = message.replace('{nome}', conv.contact_name)
                        db.close()
                    except:
                        pass  # Se não encontrar, usa mensagem original
                
                # Adiciona à fila com delay progressivo
                priority = 0  # Prioridade padrão
                message_id = queue.add_message(
                    phone=phone,
                    message=personalized_message,
                    tenant_id=session.get('tenant_id'),
                    instance_id=instance.get('id'),
                    priority=priority,
                    max_retries=3,
                    retry_delay=5
                )
                
                results["added_to_queue"] += 1
                results["message_ids"].append({
                    "phone": phone,
                    "message_id": message_id,
                    "status": "queued"
                })
                
                # Delay entre mensagens (anti-bloqueio)
                if i < len(contacts) - 1:  # Não espera após a última
                    time.sleep(delay)
                
            except Exception as e:
                logger.error(f"Erro ao adicionar contato {contact} à fila: {e}")
                results["failed"] += 1
                results["message_ids"].append({
                    "phone": str(contact),
                    "message_id": None,
                    "status": "failed",
                    "error": str(e)
                })
        
        logger.info(f"Campanha criada: {results['added_to_queue']} mensagens adicionadas à fila")
        
        return jsonify({
            "success": True,
            "message": f"Campanha criada: {results['added_to_queue']} mensagens adicionadas à fila",
            "results": results,
            "estimated_time": f"~{len(contacts) * delay / 60:.1f} minutos para enviar todas"
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao criar campanha: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@bp.route('/send-from-leads', methods=['POST'])
@require_api_auth
def send_from_leads():
    """
    Envia mensagens em massa para todos os leads de um tenant
    
    Body JSON:
    {
        "message": "Sua mensagem aqui",
        "instance_id": 1,  # opcional
        "lead_status": "NEW",  # opcional: filtrar por status
        "min_score": 0,  # opcional: filtrar por score mínimo
        "delay_between_messages": 3
    }
    """
    try:
        from flask import session
        from web.utils.instance_helper import get_or_create_user_instance
        from web.utils.auth_helpers import get_current_user_id
        from web.utils.message_queue import get_message_queue
        from src.database.db import SessionLocal
        from src.models.lead import Lead, LeadStatus
        
        data = request.get_json()
        
        message = data.get('message', '')
        instance_id = data.get('instance_id')
        lead_status = data.get('lead_status')
        min_score = data.get('min_score', 0)
        delay = data.get('delay_between_messages', 3)
        
        if not message or not message.strip():
            return jsonify({"success": False, "error": "Mensagem não pode estar vazia"}), 400
        
        # Obtém instância
        user_id = get_current_user_id() or 1
        tenant_id = session.get('tenant_id') or user_id
        
        instance = get_or_create_user_instance(user_id, instance_id)
        if not instance:
            return jsonify({"success": False, "error": "Instância não encontrada"}), 404
        
        # Busca leads
        db = SessionLocal()
        query = db.query(Lead).filter_by(tenant_id=tenant_id)
        
        if lead_status:
            try:
                status_enum = LeadStatus[lead_status.upper()]
                query = query.filter_by(status=status_enum)
            except:
                pass
        
        if min_score:
            query = query.filter(Lead.score >= min_score)
        
        leads = query.all()
        db.close()
        
        if not leads:
            return jsonify({
                "success": False,
                "error": "Nenhum lead encontrado com os filtros especificados"
            }), 404
        
        # Obtém fila
        queue = get_message_queue()
        if not queue:
            return jsonify({"success": False, "error": "Sistema de fila não disponível"}), 503
        
        # Adiciona à fila
        results = {
            "total_leads": len(leads),
            "added_to_queue": 0,
            "failed": 0
        }
        
        for i, lead in enumerate(leads):
            try:
                # Personaliza mensagem com nome do lead
                personalized_message = message.replace('{nome}', lead.name or 'Cliente')
                
                message_id = queue.add_message(
                    phone=lead.phone,
                    message=personalized_message,
                    tenant_id=tenant_id,
                    instance_id=instance.get('id'),
                    priority=0,
                    max_retries=3,
                    retry_delay=5
                )
                
                results["added_to_queue"] += 1
                
                # Delay entre mensagens
                if i < len(leads) - 1:
                    time.sleep(delay)
                    
            except Exception as e:
                logger.error(f"Erro ao adicionar lead {lead.phone} à fila: {e}")
                results["failed"] += 1
        
        return jsonify({
            "success": True,
            "message": f"Campanha criada: {results['added_to_queue']} mensagens adicionadas à fila",
            "results": results,
            "estimated_time": f"~{len(leads) * delay / 60:.1f} minutos para enviar todas"
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao criar campanha de leads: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@bp.route('/status', methods=['GET'])
@require_api_auth
def get_campaign_status():
    """
    Retorna status da fila de mensagens (quantas pendentes, processando, etc)
    """
    try:
        from web.utils.message_queue import get_message_queue
        
        queue = get_message_queue()
        if not queue:
            return jsonify({
                "success": False,
                "error": "Sistema de fila não disponível"
            }), 503
        
        return jsonify({
            "success": True,
            "queue_size": queue.get_queue_size(),
            "processing": queue.get_processing_count()
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter status da campanha: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

