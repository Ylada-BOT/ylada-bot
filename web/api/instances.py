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


from web.utils.auth_helpers import get_current_user_id, get_current_tenant_id, is_admin
from web.utils.instance_helper import get_or_create_user_instance, get_user_instance_id, update_user_instance


def get_next_available_port():
    """Obtém próxima porta disponível para instância (modo simples)"""
    # MODO SIMPLES: Calcula porta baseado nas instâncias existentes no JSON
    import json
    import os
    
    orgs_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'organizations.json')
    
    used_ports = set()
    if os.path.exists(orgs_file):
        try:
            with open(orgs_file, 'r', encoding='utf-8') as f:
                organizations = json.load(f)
                for org in organizations:
                    for instance in org.get('instances', []):
                        if instance.get('port'):
                            used_ports.add(instance['port'])
        except:
            pass
    
    base_port = 5001
    while base_port in used_ports:
        base_port += 1
    return base_port


@bp.route('', methods=['POST'])
def create_instance():
    """Cria nova instância (bot)"""
    try:
        data = request.get_json()
        
        # Validações
        name = data.get('name')
        tenant_id = data.get('tenant_id')  # organization_id
        
        if not name:
            return jsonify({
                'success': False,
                'error': 'Nome é obrigatório'
            }), 400
        if not tenant_id:
            return jsonify({
                'success': False,
                'error': 'tenant_id (organization_id) é obrigatório'
            }), 400
        
        # MODO SIMPLES: Salva em arquivo JSON (sem banco de dados)
        import json
        import os
        from datetime import datetime
        
        orgs_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'organizations.json')
        os.makedirs(os.path.dirname(orgs_file), exist_ok=True)
        
        # Carrega organizações
        organizations = []
        if os.path.exists(orgs_file):
            try:
                with open(orgs_file, 'r', encoding='utf-8') as f:
                    organizations = json.load(f)
            except:
                organizations = []
        
        # Busca organização
        org = None
        for o in organizations:
            if o.get('id') == tenant_id:
                org = o
                break
        
        if not org:
            return jsonify({
                'success': False,
                'error': 'Organização não encontrada'
            }), 404
        
        # Obtém próxima porta disponível
        port = get_next_available_port()
        
        # Calcula próximo ID da instância
        existing_instances = org.get('instances', [])
        next_instance_id = max([inst.get('id', 0) for inst in existing_instances], default=0) + 1
        
        # Cria nova instância
        new_instance = {
            'id': next_instance_id,
            'name': name,
            'status': 'disconnected',
            'port': port,
            'agent_id': data.get('agent_id'),
            'phone_number': None,
            'messages_sent': 0,
            'messages_received': 0,
            'created_at': datetime.now().isoformat(),
            'session_dir': f"data/sessions/instance_{tenant_id}_{name.lower().replace(' ', '_')}"
        }
        
        # Adiciona instância à organização
        if 'instances' not in org:
            org['instances'] = []
        org['instances'].append(new_instance)
        
        # Salva no arquivo
        with open(orgs_file, 'w', encoding='utf-8') as f:
            json.dump(organizations, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Instância criada (modo simples): {new_instance['id']} - {new_instance['name']} (porta {new_instance['port']})")
        
        return jsonify({
            'success': True,
            'instance': {
                'id': new_instance['id'],
                'name': new_instance['name'],
                'status': new_instance['status'],
                'port': new_instance['port'],
                'created_at': new_instance['created_at']
            }
        }), 201
        
        # CÓDIGO COM BANCO DE DADOS (comentado - usar depois quando precisar)
        """
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
            
            # Verifica agent_id se fornecido
            agent_id = data.get('agent_id')
            if agent_id:
                from src.models.agent import Agent
                agent = db.query(Agent).filter(
                    Agent.id == agent_id,
                    Agent.tenant_id == tenant_id
                ).first()
                if not agent:
                    return jsonify({'error': 'Agente não encontrado ou não pertence ao tenant'}), 404
            
            # Cria instância
            instance = Instance(
                tenant_id=tenant_id,
                name=name,
                status=InstanceStatus.DISCONNECTED,
                port=port,
                agent_id=agent_id,
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
        """
            
    except Exception as e:
        logger.error(f"Erro ao criar instância: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro ao criar instância',
            'message': str(e)
        }), 500


@bp.route('', methods=['GET'])
def list_instances():
    """Lista instâncias do usuário atual (modo simplificado: 1 usuário = 1 instância)"""
    try:
        user_id = get_current_user_id() or 1  # Default para desenvolvimento
        
        # No modo simplificado, cada usuário tem apenas 1 instância
        instance = get_or_create_user_instance(user_id)
        
        return jsonify({
            'success': True,
            'instances': [instance],
            'total': 1
        }), 200
        
        # CÓDIGO COM BANCO DE DADOS (comentado - usar depois quando precisar)
        """
        db = SessionLocal()
        try:
            # Obtém tenant_id do usuário atual (ou do parâmetro se for admin)
            current_tenant_id = get_current_tenant_id()
            requested_tenant_id = request.args.get('tenant_id', type=int)
            
            # Admin pode ver todos ou filtrar por tenant_id
            if is_admin():
                tenant_id = requested_tenant_id  # Admin pode escolher qual tenant ver
                if tenant_id:
                    # Verifica se tenant existe
                    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
                    if not tenant:
                        return jsonify({'error': 'Tenant não encontrado'}), 404
                    instances = db.query(Instance).filter(Instance.tenant_id == tenant_id).all()
                else:
                    # Admin vê todas as instâncias
                    instances = db.query(Instance).all()
            else:
                # Tenant só vê suas próprias instâncias
                if not current_tenant_id:
                    return jsonify({'error': 'Tenant não encontrado para o usuário'}), 404
                tenant_id = current_tenant_id
                instances = db.query(Instance).filter(Instance.tenant_id == tenant_id).all()
            
            result = []
            for instance in instances:
                result.append({
                    'id': instance.id,
                    'name': instance.name,
                    'status': instance.status.value,
                    'port': instance.port,
                    'phone_number': instance.phone_number,
                    'agent_id': instance.agent_id,
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
        """
            
    except Exception as e:
        logger.error(f"Erro ao listar instâncias: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro ao listar instâncias',
            'message': str(e)
        }), 500


@bp.route('/<int:instance_id>', methods=['GET'])
def get_instance(instance_id):
    """Obtém detalhes da instância (modo simplificado: retorna instância do usuário)"""
    try:
        user_id = get_current_user_id() or 1
        
        # No modo simplificado, verifica se é a instância do usuário
        instance = get_or_create_user_instance(user_id)
        
        if instance.get('id') != instance_id:
            return jsonify({
                'success': False,
                'error': 'Instância não encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'instance': instance
        }), 200
        
        # CÓDIGO COM BANCO DE DADOS (comentado - usar depois quando precisar)
        """
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
                    'agent_id': instance.agent_id,
                    'messages_sent': instance.messages_sent,
                    'messages_received': instance.messages_received,
                    'last_message_at': instance.last_message_at.isoformat() if instance.last_message_at else None,
                    'created_at': instance.created_at.isoformat(),
                    'tenant_id': instance.tenant_id
                }
            }), 200
            
        finally:
            db.close()
        """
            
    except Exception as e:
        logger.error(f"Erro ao obter instância: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro ao obter instância',
            'message': str(e)
        }), 500


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
            if 'agent_id' in data:
                agent_id = data['agent_id']
                if agent_id:
                    # Verifica se agente existe e pertence ao tenant
                    from src.models.agent import Agent
                    agent = db.query(Agent).filter(
                        Agent.id == agent_id,
                        Agent.tenant_id == instance.tenant_id
                    ).first()
                    if not agent:
                        return jsonify({'error': 'Agente não encontrado ou não pertence ao tenant'}), 404
                instance.agent_id = agent_id
            
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
    """Obtém status da conexão WhatsApp da instância (modo simplificado)"""
    try:
        import requests
        
        user_id = get_current_user_id() or 1
        
        # Verifica se é a instância do usuário
        instance = get_or_create_user_instance(user_id)
        
        if instance.get('id') != instance_id:
            return jsonify({
                'success': False,
                'error': 'Instância não encontrada'
            }), 404
        
        # Verifica conexão com servidor Node.js
        port = instance.get('port', 5001)
        try:
            response = requests.get(f"http://localhost:{port}/status", timeout=2)
            if response.status_code == 200:
                server_status = response.json()
                has_qr = server_status.get("hasQr", False)
                actually_connected = server_status.get("actuallyConnected", False)
                ready = server_status.get("ready", False)
                
                # Verifica se realmente está conectado
                is_connected = False
                if actually_connected:
                    # Se actually_connected existe (não é False/None), está conectado
                    is_connected = True
                elif ready:
                    # Se ready existe e não tem QR, também está conectado
                    if isinstance(ready, dict) or ready is True:
                        is_connected = True
                
                # Extrai número do telefone se estiver conectado
                phone_number = None
                if is_connected:
                    # Tenta obter o número do telefone do objeto actually_connected ou ready
                    if isinstance(actually_connected, dict) and 'user' in actually_connected:
                        phone_number = actually_connected.get('user')
                    elif isinstance(ready, dict) and 'user' in ready:
                        phone_number = ready.get('user')
                    
                    # Formata o número para exibição
                    if phone_number:
                        # Remove @c.us se houver
                        phone_number = phone_number.replace('@c.us', '').replace('@s.whatsapp.net', '')
                        # Formata número brasileiro (se começar com 55)
                        if phone_number.startswith('55') and len(phone_number) >= 12:
                            formatted = f"+{phone_number[:2]} ({phone_number[2:4]}) {phone_number[4:9]}-{phone_number[9:]}"
                            phone_number = formatted
                        else:
                            phone_number = f"+{phone_number}"
                
                return jsonify({
                    'success': True,
                    'connected': is_connected,
                    'has_qr': has_qr,
                    'status': instance.get('status', 'disconnected'),
                    'phone_number': phone_number
                }), 200
        except requests.exceptions.ConnectionError:
            return jsonify({
                'success': True,
                'connected': False,
                'has_qr': False,
                'status': instance.get('status', 'disconnected'),
                'message': f'Servidor WhatsApp não está rodando na porta {port}'
            }), 200
        except Exception as e:
            logger.error(f"Erro ao verificar status: {e}")
        
        # Se servidor não está respondendo
        return jsonify({
            'success': True,
            'connected': False,
            'has_qr': False,
            'status': instance.get('status', 'disconnected'),
            'message': 'Servidor WhatsApp não está rodando'
        }), 200
        
        # CÓDIGO COM BANCO DE DADOS (comentado - usar depois quando precisar)
        """
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
        """
            
    except Exception as e:
        logger.error(f"Erro ao obter status: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro ao obter status',
            'message': str(e)
        }), 500


@bp.route('/<int:instance_id>/qr', methods=['GET'])
def get_instance_qr(instance_id):
    """Obtém QR Code da instância"""
    try:
        # Modo simplificado: usa helper
        import requests
        
        user_id = get_current_user_id() or 1
        instance = get_or_create_user_instance(user_id)
        
        if instance.get('id') != instance_id:
            return jsonify({
                'success': False,
                'error': 'Instância não encontrada'
            }), 404
        
        # Busca QR Code do servidor Node.js
        port = instance.get('port', 5001)
        try:
            response = requests.get(f"http://localhost:{port}/qr", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return jsonify({
                    'success': True,
                    'qr': data.get('qr'),
                    'ready': data.get('ready', False)
                }), 200
        except requests.exceptions.ConnectionError:
            return jsonify({
                'success': False,
                'error': f'Servidor WhatsApp não está rodando na porta {port}. Inicie o servidor primeiro.'
            }), 503
        except Exception as e:
            logger.error(f"Erro ao buscar QR Code: {e}")
            return jsonify({
                'success': False,
                'error': f'Erro ao conectar com servidor WhatsApp: {str(e)}'
            }), 503
        
        return jsonify({
            'success': False,
            'error': 'Servidor WhatsApp não está respondendo. Inicie o servidor primeiro.'
        }), 503
        
        # CÓDIGO COM BANCO DE DADOS (comentado - usar depois quando precisar)
        """
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
        """
            
    except Exception as e:
        logger.error(f"Erro ao obter QR Code: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro ao obter QR Code',
            'message': str(e)
        }), 500


