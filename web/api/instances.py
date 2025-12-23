"""
APIs de Instâncias (Bots)
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from src.database.db import SessionLocal
from src.models.instance import Instance, InstanceStatus
from src.models.tenant import Tenant
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)

bp = Blueprint('instances', __name__, url_prefix='/api/instances')


def get_current_user_id():
    """Obtém ID do usuário atual da sessão"""
    from flask import session
    return session.get('user_id')


def get_next_available_port():
    """Obtém próxima porta disponível para instância"""
    # Começa na 5001 e vai incrementando
    # Em produção, você pode usar um sistema mais sofisticado
    db = SessionLocal()
    try:
        instances = db.query(Instance).all()
        used_ports = {inst.port for inst in instances if inst.port}
        base_port = 5001
        while base_port in used_ports:
            base_port += 1
        return base_port
    finally:
        db.close()


@bp.route('', methods=['POST'])
def create_instance():
    """Cria nova instância (bot)"""
    try:
        data = request.get_json()
        
        # Validações
        name = data.get('name')
        tenant_id = data.get('tenant_id')
        
        if not name:
            return jsonify({'error': 'Nome é obrigatório'}), 400
        if not tenant_id:
            return jsonify({'error': 'tenant_id é obrigatório'}), 400
        
        db = SessionLocal()
        try:
            # Verifica se tenant existe
            tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
            if not tenant:
                return jsonify({'error': 'Tenant não encontrado'}), 404
            
            # Verifica se usuário tem acesso ao tenant
            user_id = get_current_user_id()
            if user_id and tenant.user_id != user_id:
                return jsonify({'error': 'Acesso negado'}), 403
            
            # Obtém próxima porta disponível
            port = get_next_available_port()
            
            # Cria instância
            instance = Instance(
                tenant_id=tenant_id,
                name=name,
                status=InstanceStatus.DISCONNECTED,
                port=port,
                session_dir=f"data/sessions/instance_{tenant_id}_{name.lower().replace(' ', '_')}"
            )
            
            db.add(instance)
            db.commit()
            db.refresh(instance)
            
            logger.info(f"Instância criada: {instance.id} - {instance.name} (porta {instance.port})")
            
            return jsonify({
                'success': True,
                'instance': {
                    'id': instance.id,
                    'name': instance.name,
                    'status': instance.status.value,
                    'port': instance.port,
                    'created_at': instance.created_at.isoformat()
                }
            }), 201
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao criar instância: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('', methods=['GET'])
def list_instances():
    """Lista instâncias"""
    try:
        tenant_id = request.args.get('tenant_id', type=int)
        
        if not tenant_id:
            return jsonify({'error': 'tenant_id é obrigatório'}), 400
        
        db = SessionLocal()
        try:
            # Verifica se tenant existe
            tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
            if not tenant:
                return jsonify({'error': 'Tenant não encontrado'}), 404
            
            # Verifica se usuário tem acesso
            user_id = get_current_user_id()
            if user_id and tenant.user_id != user_id:
                return jsonify({'error': 'Acesso negado'}), 403
            
            # Busca instâncias do tenant
            instances = db.query(Instance).filter(Instance.tenant_id == tenant_id).all()
            
            result = []
            for instance in instances:
                result.append({
                    'id': instance.id,
                    'name': instance.name,
                    'status': instance.status.value,
                    'port': instance.port,
                    'phone_number': instance.phone_number,
                    'messages_sent': instance.messages_sent,
                    'messages_received': instance.messages_received,
                    'created_at': instance.created_at.isoformat()
                })
            
            return jsonify({
                'success': True,
                'instances': result,
                'total': len(result)
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao listar instâncias: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:instance_id>', methods=['GET'])
def get_instance(instance_id):
    """Obtém detalhes da instância"""
    try:
        db = SessionLocal()
        try:
            instance = db.query(Instance).filter(Instance.id == instance_id).first()
            
            if not instance:
                return jsonify({'error': 'Instância não encontrada'}), 404
            
            # Verifica se usuário tem acesso
            tenant = db.query(Tenant).filter(Tenant.id == instance.tenant_id).first()
            user_id = get_current_user_id()
            if user_id and tenant.user_id != user_id:
                return jsonify({'error': 'Acesso negado'}), 403
            
            return jsonify({
                'success': True,
                'instance': {
                    'id': instance.id,
                    'name': instance.name,
                    'status': instance.status.value,
                    'port': instance.port,
                    'phone_number': instance.phone_number,
                    'messages_sent': instance.messages_sent,
                    'messages_received': instance.messages_received,
                    'last_message_at': instance.last_message_at.isoformat() if instance.last_message_at else None,
                    'created_at': instance.created_at.isoformat(),
                    'tenant_id': instance.tenant_id
                }
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao obter instância: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:instance_id>', methods=['PUT'])
def update_instance(instance_id):
    """Atualiza instância"""
    try:
        data = request.get_json()
        
        db = SessionLocal()
        try:
            instance = db.query(Instance).filter(Instance.id == instance_id).first()
            
            if not instance:
                return jsonify({'error': 'Instância não encontrada'}), 404
            
            # Verifica se usuário tem acesso
            tenant = db.query(Tenant).filter(Tenant.id == instance.tenant_id).first()
            user_id = get_current_user_id()
            if user_id and tenant.user_id != user_id:
                return jsonify({'error': 'Acesso negado'}), 403
            
            # Atualiza campos
            if 'name' in data:
                instance.name = data['name']
            if 'status' in data:
                instance.status = InstanceStatus(data['status'])
            
            instance.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(instance)
            
            logger.info(f"Instância atualizada: {instance.id}")
            
            return jsonify({
                'success': True,
                'instance': {
                    'id': instance.id,
                    'name': instance.name,
                    'status': instance.status.value
                }
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao atualizar instância: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:instance_id>', methods=['DELETE'])
def delete_instance(instance_id):
    """Deleta instância"""
    try:
        db = SessionLocal()
        try:
            instance = db.query(Instance).filter(Instance.id == instance_id).first()
            
            if not instance:
                return jsonify({'error': 'Instância não encontrada'}), 404
            
            # Verifica se usuário tem acesso
            tenant = db.query(Tenant).filter(Tenant.id == instance.tenant_id).first()
            user_id = get_current_user_id()
            if user_id and tenant.user_id != user_id:
                return jsonify({'error': 'Acesso negado'}), 403
            
            # TODO: Parar servidor Node.js se estiver rodando
            
            # Deleta instância
            db.delete(instance)
            db.commit()
            
            logger.info(f"Instância deletada: {instance_id}")
            
            return jsonify({
                'success': True,
                'message': 'Instância deletada com sucesso'
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao deletar instância: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:instance_id>/status', methods=['GET'])
def get_instance_status(instance_id):
    """Obtém status da conexão WhatsApp da instância"""
    try:
        db = SessionLocal()
        try:
            instance = db.query(Instance).filter(Instance.id == instance_id).first()
            
            if not instance:
                return jsonify({'error': 'Instância não encontrada'}), 404
            
            # Verifica conexão com servidor Node.js
            import requests
            try:
                response = requests.get(f"http://localhost:{instance.port}/status", timeout=2)
                if response.status_code == 200:
                    server_status = response.json()
                    return jsonify({
                        'success': True,
                        'connected': server_status.get('ready', False),
                        'has_qr': server_status.get('hasQr', False),
                        'status': instance.status.value
                    }), 200
            except:
                pass
            
            # Se servidor não está respondendo
            return jsonify({
                'success': True,
                'connected': False,
                'has_qr': False,
                'status': instance.status.value,
                'message': 'Servidor WhatsApp não está rodando'
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao obter status: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:instance_id>/qr', methods=['GET'])
def get_instance_qr(instance_id):
    """Obtém QR Code da instância"""
    try:
        db = SessionLocal()
        try:
            instance = db.query(Instance).filter(Instance.id == instance_id).first()
            
            if not instance:
                return jsonify({'error': 'Instância não encontrada'}), 404
            
            # Busca QR Code do servidor Node.js
            import requests
            try:
                response = requests.get(f"http://localhost:{instance.port}/qr", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    return jsonify({
                        'success': True,
                        'qr': data.get('qr'),
                        'ready': data.get('ready', False)
                    }), 200
            except Exception as e:
                logger.error(f"Erro ao buscar QR Code: {e}")
            
            return jsonify({
                'success': False,
                'error': 'Servidor WhatsApp não está respondendo. Inicie o servidor primeiro.'
            }), 503
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao obter QR Code: {e}")
        return jsonify({'error': str(e)}), 500

